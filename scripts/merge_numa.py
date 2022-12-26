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
            print(f"Merge Numa Process: {line}")
            rs = line.rstrip("\r\n").split("\t")

            # unpack(ハッシュは対応しない)
            try:
                model_0 = rs[0]
                model_1 = rs[2]
                if shared.cmd_opts.ckpt_dir:
                    output_file = os.path.join(shared.cmd_opts.ckpt_dir, rs[4])
                else:
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
                print("Log format: MBW (Classic)")
                bw = importlib.import_module("extensions.sdweb-merge-block-weighted-gui.scripts.mbw.merge_block_weighted")
                merge = getattr(bw, 'merge')
                merge(weights1, model_0, model_1, device, base_alpha, output_file, allow_overwrite, verbose)
            else:
                print("Log format: MBW Each")
                bw = importlib.import_module("extensions.sdweb-merge-block-weighted-gui.scripts.mbw_each.merge_block_weighted_mod")
                merge = getattr(bw, 'merge')
                merge(weights1, weights2, model_0, model_1, device, base_alpha, output_file, allow_overwrite, verbose)

            # モデルが増えたので一覧更新
            sd_models.list_models()

            # マージできたモデルに切り替え
            hit = False
            for c in sd_models.checkpoints_list.values():
                if c.filename == output_file:
                    print(f"Use Model: {c.filename}")
                    p.override_settings['sd_model_checkpoint'] = c.title
                    hit = True
            if not hit:
                # あいまいな検索
                searchString = os.path.splitext(os.path.basename(output_file))[0]
                c = sd_models.get_closet_checkpoint_match(searchString)
                if c is not None:
                    print(f"Matched Model: {c.filename}")
                    p.override_settings['sd_model_checkpoint'] = c.title
                    hit = True
            if not hit:
                raise ValueError(f"Model {output_file} not in checkpoints_list")

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
