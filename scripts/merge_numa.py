import os
import random
import re
import pathlib
import importlib

import gradio as gr

from modules import scripts, script_callbacks, shared
from modules import sd_models
from modules.processing import Processed, process_images

class Script(scripts.Script):
    def title(self):
        return "Merge Numa"
    
    def ui(self, is_img2img):
        batch = gr.Textbox(lines=10,label="Batch(History Format, without Header)")
        each_delete = gr.Checkbox(value=True,label="Delete Merged Model each time")
        return [batch, each_delete]

    def on_show(self, batch):
        return [gr.Textbox.update(visible=True),
                gr.Button.update(visible=True),
                gr.Checkbox.update(visible=True),
                ]

    def run(self, p, batch, each_delete):
        images = []
        # 1行につき1モデルと1画像を作成する
        for line in batch.split("\n"):
            rs = line.rstrip("\r\n").split("\t")
            if len(rs) != 9:
                raise ValueError(f"Unknown format: {line}")

            # unpack(ハッシュは対応しない)
            model_0 = rs[0]
            model_1 = rs[2]
            output_file = os.path.join('models', 'Stable-diffusion', rs[4])
            base_alpha = float(rs[6])
            weights = rs[8]
        
            # ハイフンのあるディレクトリのインポート
            bw = importlib.import_module(f"extensions.sdweb-merge-block-weighted-gui.scripts.merge_block_weighted")
            merge = getattr(bw, 'merge')

            # 引数
            device = "cpu" # devices.get_optimal_device()
            allow_overwrite=True
            verbose=False

            merge(weights, model_0, model_1, device, base_alpha, output_file, allow_overwrite, verbose)

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
