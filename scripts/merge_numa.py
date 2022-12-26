import os
import random
import re
import pathlib
import importlib

import gradio as gr

from modules import scripts, script_callbacks, shared
from modules import sd_models, devices
from modules.processing import Processed, process_images

class Script(scripts.Script):
    def title(self):
        return "Merge Numa"
    
    def ui(self, is_img2img):
        batch = gr.Textbox(lines=10,label="Batch(History Format, without Header)")
        each_delete = gr.Checkbox(value=True,label="Delete Merged Model each time")
        use_cpu = gr.Checkbox(value=True,label="Use CPU")
        return [batch, each_delete, use_cpu]

    def on_show(self, batch):
        return [gr.Textbox.update(visible=True),
                gr.Button.update(visible=True),
                gr.Checkbox.update(visible=True),
                ]

    def run(self, p, batch, each_delete, use_cpu):
        images = []
        # 1行につき1モデルと1画像を作成する
        for line in batch.split("\n"):
            rs = line.rstrip("\r\n").split("\t")

            # unpack(ハッシュは対応しない)
            try:
                model_0 = rs[0]
                model_1 = rs[2]
                output_file = os.path.join(sd_models.model_path, rs[4])
                base_alpha = float(rs[6])
                weights1 = rs[8]
            except:
                raise ValueError(f"Unknown format: {rs}")

            try:
                weights2 = rs[9]
            except:
                pass

            # 引数
            if use_cpu:
                device = "cpu"
            else:
                device = devices.get_optimal_device()
            allow_overwrite=True
            verbose=False

            # ハイフンのあるディレクトリのインポート
            if not weights2:
                # MBW
                bw = importlib.import_module("extensions.sdweb-merge-block-weighted-gui.scripts.mbw.merge_block_weighted")
                merge = getattr(bw, 'merge')
                merge(weights1, model_0, model_1, device, base_alpha, output_file, allow_overwrite, verbose)
            else:
                # MBW each
                bw = importlib.import_module("extensions.sdweb-merge-block-weighted-gui.scripts.mbw_each.merge_block_weighted_mod")
                merge = getattr(bw, 'merge')
                merge(weights1, weights2, model_0, model_1, device, base_alpha, output_file, allow_overwrite, verbose)

            # モデルが増えたので一覧更新
            sd_models.list_models()

            # マージできたモデルに切り替え
            for c in sd_models.checkpoints_list.values():
                if c.filename.find(output_file) != 1:
                    p.override_settings['sd_model_checkpoint'] = c.title

            # サンプルにログを残す
            p.extra_generation_params["Mergelog"] = line

            # サンプル生成
            proc = process_images(p)
            images += proc.images

            # 作ったモデルを消す
            if each_delete:
                if os.path.exists(output_file):
                    print(f"Delete {output_file}")
                    os.remove(output_file)

        return Processed(p, images, p.seed, "")
