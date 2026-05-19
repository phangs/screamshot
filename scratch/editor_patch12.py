import sys

filepath = "/home/phangs/Development/Personal/screamshot/src/main.rs"

with open(filepath, "r") as f:
    content = f.read()

# 1. Update find_resize_handle to support Annotation::Text
old_find_resize = """fn find_resize_handle(ann: &Annotation, local_pos: egui::Pos2) -> Option<ResizeHandle> {
    let rect = match ann {
        Annotation::Rectangle { rect, .. } => *rect,
        Annotation::Blur { rect } => *rect,
        _ => return None,
    };"""

new_find_resize = """fn find_resize_handle(ann: &Annotation, local_pos: egui::Pos2) -> Option<ResizeHandle> {
    let rect = match ann {
        Annotation::Rectangle { rect, .. } => *rect,
        Annotation::Blur { rect } => *rect,
        Annotation::Text { pos, text, size, .. } => {
            let char_width = *size;
            let text_w = text.len() as f32 * char_width * 0.85;
            egui::Rect::from_center_size(*pos, egui::vec2(text_w.max(30.0), char_width * 1.5)).expand(4.0)
        }
        _ => return None,
    };"""

if old_find_resize in content:
    content = content.replace(old_find_resize, new_find_resize)
    print("find_resize_handle helper updated!")
else:
    print("Error: find_resize_handle helper not found!")

# 2. Update pointer dragged handler to support Annotation::Text resizing
old_resized_match = """                                                match ann {
                                                    Annotation::Rectangle { rect: r, .. } => *r = rect,
                                                    Annotation::Blur { rect: r } => *r = rect,
                                                    _ => {}
                                                }
                                            }
                                        }
                                    } else if let Some(idx) = self.editor_dragged_annotation {"""

new_resized_match = """                                                match ann {
                                                    Annotation::Rectangle { rect: r, .. } => *r = rect,
                                                    Annotation::Blur { rect: r } => *r = rect,
                                                    _ => {}
                                                }
                                            }
                                        }
                                        Annotation::Text { pos, text, size, .. } => {
                                            let l = text.len() as f32;
                                            let half_w = (l * 0.85 / 2.0).max(15.0 / *size);
                                            let half_h = 1.5 / 2.0;
                                            let factor = (half_w * half_w + half_h * half_h).sqrt();
                                            let d = local.distance(*pos);
                                            *size = (d / factor).clamp(10.0, 150.0);
                                        }
                                        _ => {}
                                    }
                                    if let Some(ann) = self.editor_annotations.get(idx) {
                                        if let Annotation::Text { .. } = ann {
                                            // Handled already
                                        }
                                    }
                                } else if let Some(idx) = self.editor_dragged_annotation {"""

if old_resized_match in content:
    content = content.replace(old_resized_match, new_resized_match)
    print("Pointer dragged handler updated!")
else:
    old_resized_match_win = old_resized_match.replace("\n", "\r\n")
    if old_resized_match_win in content:
        content = content.replace(old_resized_match_win, new_resized_match)
        print("Pointer dragged handler updated (Win)!")
    else:
        print("Error: Pointer dragged handler not found!")

# 3. Update pointer dragged handler's outer if let block
old_resized_outer = """                                    if let Some(idx) = self.editor_resized_annotation {
                                        if let Some(ann) = self.editor_annotations.get_mut(idx) {
                                            let mut rect = match ann {
                                                Annotation::Rectangle { rect, .. } => *rect,
                                                Annotation::Blur { rect } => *rect,
                                                _ => egui::Rect::NOTHING,
                                            };
                                            if rect != egui::Rect::NOTHING {
                                                if let Some(handle) = self.editor_resize_handle {
                                                    match handle {
                                                        ResizeHandle::TopLeft => {
                                                            rect.min.x = local.x.min(rect.max.x - 5.0);
                                                            rect.min.y = local.y.min(rect.max.y - 5.0);
                                                        }
                                                        ResizeHandle::TopRight => {
                                                            rect.max.x = local.x.max(rect.min.x + 5.0);
                                                            rect.min.y = local.y.min(rect.max.y - 5.0);
                                                        }
                                                        ResizeHandle::BottomLeft => {
                                                            rect.min.x = local.x.min(rect.max.x - 5.0);
                                                            rect.max.y = local.y.max(rect.min.y + 5.0);
                                                        }
                                                        ResizeHandle::BottomRight => {
                                                            rect.max.x = local.x.max(rect.min.x + 5.0);
                                                            rect.max.y = local.y.max(rect.min.y + 5.0);
                                                        }
                                                    }
                                                }
                                                match ann {
                                                    Annotation::Rectangle { rect: r, .. } => *r = rect,
                                                    Annotation::Blur { rect: r } => *r = rect,
                                                    _ => {}
                                                }
                                            }
                                        }
                                    } else if let Some(idx) = self.editor_dragged_annotation {"""

new_resized_outer = """                                    if let Some(idx) = self.editor_resized_annotation {
                                        let mut rect = egui::Rect::NOTHING;
                                        if let Some(ann) = self.editor_annotations.get_mut(idx) {
                                            match ann {
                                                Annotation::Rectangle { rect: r, .. } => rect = *r,
                                                Annotation::Blur { rect: r } => rect = *r,
                                                _ => {}
                                            }
                                        }
                                        if rect != egui::Rect::NOTHING {
                                            if let Some(handle) = self.editor_resize_handle {
                                                match handle {
                                                    ResizeHandle::TopLeft => {
                                                        rect.min.x = local.x.min(rect.max.x - 5.0);
                                                        rect.min.y = local.y.min(rect.max.y - 5.0);
                                                    }
                                                    ResizeHandle::TopRight => {
                                                        rect.max.x = local.x.max(rect.min.x + 5.0);
                                                        rect.min.y = local.y.min(rect.max.y - 5.0);
                                                    }
                                                    ResizeHandle::BottomLeft => {
                                                        rect.min.x = local.x.min(rect.max.x - 5.0);
                                                        rect.max.y = local.y.max(rect.min.y + 5.0);
                                                    }
                                                    ResizeHandle::BottomRight => {
                                                        rect.max.x = local.x.max(rect.min.x + 5.0);
                                                        rect.max.y = local.y.max(rect.min.y + 5.0);
                                                    }
                                                }
                                            }
                                            if let Some(ann) = self.editor_annotations.get_mut(idx) {
                                                match ann {
                                                    Annotation::Rectangle { rect: r, .. } => *r = rect,
                                                    Annotation::Blur { rect: r } => *r = rect,
                                                    _ => {}
                                                }
                                            }
                                        } else {
                                            if let Some(ann) = self.editor_annotations.get_mut(idx) {
                                                if let Annotation::Text { pos, text, size, .. } = ann {
                                                    let l = text.len() as f32;
                                                    let half_w = (l * 0.85 / 2.0).max(15.0 / *size);
                                                    let half_h = 1.5 / 2.0;
                                                    let factor = (half_w * half_w + half_h * half_h).sqrt();
                                                    let d = local.distance(*pos);
                                                    *size = (d / factor).clamp(10.0, 150.0);
                                                }
                                            }
                                        }
                                    } else if let Some(idx) = self.editor_dragged_annotation {"""

if old_resized_outer in content:
    content = content.replace(old_resized_outer, new_resized_outer)
    print("Outer pointer dragged handler updated!")
else:
    old_resized_outer_win = old_resized_outer.replace("\n", "\r\n")
    if old_resized_outer_win in content:
        content = content.replace(old_resized_outer_win, new_resized_outer)
        print("Outer pointer dragged handler updated (Win)!")
    else:
        print("Error: Outer pointer dragged handler not found!")

# 4. Add corner resize circles to Text Annotation Selection UI drawing
old_text_ui = """                                            let cx = handle_rect.center().x;
                                            let cy = handle_rect.center().y;
                                            for dx in [-4.0, 0.0, 4.0] {
                                                ui.painter().circle_filled(
                                                    egui::pos2(cx + dx, cy),
                                                    1.5,
                                                    egui::Color32::WHITE
                                                );
                                            }
                                        }"""

new_text_ui = """                                            let cx = handle_rect.center().x;
                                            let cy = handle_rect.center().y;
                                            for dx in [-4.0, 0.0, 4.0] {
                                                ui.painter().circle_filled(
                                                    egui::pos2(cx + dx, cy),
                                                    1.5,
                                                    egui::Color32::WHITE
                                                );
                                            }
                                            // Draw four corner resize handles
                                            let corners = [
                                                bounds.min,
                                                egui::pos2(bounds.max.x, bounds.min.y),
                                                egui::pos2(bounds.min.x, bounds.max.y),
                                                bounds.max
                                            ];
                                            for cp in corners {
                                                ui.painter().circle_filled(cp, 5.0, egui::Color32::from_rgb(0, 160, 255));
                                                ui.painter().circle_stroke(cp, 5.0, egui::Stroke::new(1.5, egui::Color32::WHITE));
                                            }
                                        }"""

if old_text_ui in content:
    content = content.replace(old_text_ui, new_text_ui)
    print("Text Selection UI handles added!")
else:
    old_text_ui_win = old_text_ui.replace("\n", "\r\n")
    if old_text_ui_win in content:
        content = content.replace(old_text_ui_win, new_text_ui)
        print("Text Selection UI handles added (Win)!")
    else:
        print("Error: Text Selection UI handles not found!")

# Write file back
with open(filepath, "w") as f:
    f.write(content)

print("Patch 12 completed successfully!")
