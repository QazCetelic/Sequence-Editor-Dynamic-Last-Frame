import bpy

enabled_global = False

def adjust_last_frame():
    if enabled_global:
        scene = bpy.data.scenes["Scene"]
        editor = scene.sequence_editor

        last_frame = 0
        for sequence in editor.sequences_all:
            if sequence.frame_final_end > last_frame:
                last_frame = sequence.frame_final_end

        if last_frame != scene.frame_end:
            print(f"Adjusting last frame from {scene.frame_end} to {last_frame}!")
            scene.frame_end = last_frame

    return 0.1 # execute every 100ms

bpy.app.timers.register(adjust_last_frame)

class DynamicLastFrameOperator(bpy.types.Operator):
    bl_idname = "video.dynamic_frame"
    bl_label = "Dynamic Last Frame"

    enabled: bpy.props.BoolProperty(name="Enabled")

    def execute(self, context):
        global enabled_global
        enabled_global = self.enabled
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "enabled")

# Only needed if you want to add into a dynamic menu.
def menu_func(self, context):
    self.layout.operator(DynamicLastFrameOperator.bl_idname, text="Dynamic Last Frame Operator")


# Register and add to the view menu (required to also use F3 search "Dynamic Last Frame Operator" for quick access).
bpy.utils.register_class(DynamicLastFrameOperator)
bpy.types.VIEW3D_MT_view.append(menu_func)

# Test call to the newly defined operator.
bpy.ops.video.dynamic_frame()
