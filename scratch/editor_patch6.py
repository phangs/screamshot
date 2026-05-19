import sys

filepath = "/home/phangs/Development/Personal/screamshot/src/main.rs"

with open(filepath, "r") as f:
    content = f.read()

# 1. Add editor_editing_text_index to ScreamshotApp struct
old_struct = """    editor_step_count: usize,
    editor_text_input: String,
}"""
new_struct = """    editor_step_count: usize,
    editor_text_input: String,
    editor_editing_text_index: Option<usize>,
}"""

if old_struct in content:
    content = content.replace(old_struct, new_struct)
    print("ScreamshotApp struct updated!")
else:
    # Win line endings check
    old_struct_win = old_struct.replace("\n", "\r\n")
    if old_struct_win in content:
        content = content.replace(old_struct_win, new_struct)
        print("ScreamshotApp struct updated (Win)!")
    else:
        print("Error struct not found!")

# 2. Add editor_editing_text_index initializer to ScreamshotApp::new()
old_init = """            editor_step_count: 1,
            editor_text_input: String::new(),
        }"""
new_init = """            editor_step_count: 1,
            editor_text_input: String::new(),
            editor_editing_text_index: None,
        }"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("ScreamshotApp::new updated!")
else:
    old_init_win = old_init.replace("\n", "\r\n")
    if old_init_win in content:
        content = content.replace(old_init_win, new_init)
        print("ScreamshotApp::new updated (Win)!")
    else:
        print("Error initializer not found!")

# 3. Reset editor_editing_text_index inside image_receiver block
old_recv = """            self.editor_step_count = 1;
            self.editor_text_input = String::new();
            self.state = AppState::EditingCapture;"""
new_recv = """            self.editor_step_count = 1;
            self.editor_text_input = String::new();
            self.editor_editing_text_index = None;
            self.state = AppState::EditingCapture;"""

if old_recv in content:
    content = content.replace(old_recv, new_recv)
    print("Image receiver block updated!")
else:
    old_recv_win = old_recv.replace("\n", "\r\n")
    if old_recv_win in content:
        content = content.replace(old_recv_win, new_recv)
        print("Image receiver block updated (Win)!")
    else:
        print("Error image receiver block not found!")

# 4. Replace side panel Text content editor with a tip
old_side = """                    if self.editor_tool == EditorTool::Text {
                        ui.add_space(15.0);
                        ui.label("Text Content:");
                        ui.text_edit_singleline(&mut self.editor_text_input);
                    }"""

new_side = """                    if self.editor_tool == EditorTool::Text {
                        ui.add_space(10.0);
                        ui.colored_label(egui::Color32::from_rgb(0, 160, 255), "💡 Text Tool Active");
                        ui.add_space(5.0);
                        ui.label("Click anywhere on the screenshot to add text, or click an existing text block to edit it!");
                    }"""

if old_side in content:
    content = content.replace(old_side, new_side)
    print("Side panel text tip updated!")
else:
    old_side_win = old_side.replace("\n", "\r\n")
    if old_side_win in content:
        content = content.replace(old_side_win, new_side)
        print("Side panel text tip updated (Win)!")
    else:
        print("Error side panel block not found!")

# 5. Replace response.clicked() for Text tool
old_click = """                                } else if self.editor_tool == EditorTool::Text {
                                    if !self.editor_text_input.is_empty() {
                                        self.editor_annotations.push(Annotation::Text {
                                            pos: local,
                                            text: self.editor_text_input.clone(),
                                            color: self.editor_color,
                                            size: (self.editor_stroke_width * 3.0).max(10.0),
                                        });
                                    }
                                }"""

new_click = """                                } else if self.editor_tool == EditorTool::Text {
                                    let mut clicked_existing = false;
                                    for (i, ann) in self.editor_annotations.iter().enumerate() {
                                        if let Annotation::Text { pos, text, size, .. } = ann {
                                            let dist = local.distance(*pos);
                                            let text_w = text.len() as f32 * (*size * 0.6);
                                            if dist < text_w.max(25.0) {
                                                self.editor_editing_text_index = Some(i);
                                                clicked_existing = true;
                                                break;
                                            }
                                        }
                                    }
                                    if !clicked_existing {
                                        let new_idx = self.editor_annotations.len();
                                        self.editor_annotations.push(Annotation::Text {
                                            pos: local,
                                            text: String::new(),
                                            color: self.editor_color,
                                            size: (self.editor_stroke_width * 3.0).max(14.0),
                                        });
                                        self.editor_editing_text_index = Some(new_idx);
                                    }
                                }"""

if old_click in content:
    content = content.replace(old_click, new_click)
    print("Canvas click text handler updated!")
else:
    old_click_win = old_click.replace("\n", "\r\n")
    if old_click_win in content:
        content = content.replace(old_click_win, new_click)
        print("Canvas click text handler updated (Win)!")
    else:
        print("Error canvas click text handler not found!")

# 6. Update Egui Painter for Annotation::Text to draw translucent backing box
old_paint = """                                Annotation::Text { pos, text, color, size } => {
                                    let center = to_screen(*pos);
                                    let font_size = *size * (image_rect.width() / img_w);
                                    ui.painter().text(
                                        center,
                                        egui::Align2::CENTER_CENTER,
                                        text,
                                        egui::FontId::proportional(font_size.max(10.0)),
                                        *color,
                                    );
                                }"""

new_paint = """                                Annotation::Text { pos, text, color, size } => {
                                    let center = to_screen(*pos);
                                    let font_size = *size * (image_rect.width() / img_w);
                                    let font_id = egui::FontId::proportional(font_size.max(10.0));
                                    
                                    if !text.is_empty() {
                                        let galley = ui.painter().layout_no_wrap(text.clone(), font_id.clone(), *color);
                                        let rect = galley.rect.translate(center.to_vec2() - galley.rect.center().to_vec2());
                                        ui.painter().rect_filled(rect.expand(4.0), 3.0, egui::Color32::from_black_alpha(120));
                                        ui.painter().galley(rect.min, galley);
                                    }
                                }"""

if old_paint in content:
    content = content.replace(old_paint, new_paint)
    print("Egui text painter updated!")
else:
    old_paint_win = old_paint.replace("\n", "\r\n")
    if old_paint_win in content:
        content = content.replace(old_paint_win, new_paint)
        print("Egui text painter updated (Win)!")
    else:
        print("Error egui text painter not found!")

# Write file back
with open(filepath, "w") as f:
    f.write(content)

print("Patch 6 completed!")
