# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.app.handlers import persistent
from bpy.props import BoolProperty

bl_info = {
    "name": "SimpleVisibility",
    "description": "Sets every objects render-visibility to be in sync with viewport-visibility",
    "author": "Debuk",
    "version": (1, 1, 2),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Object"    
}


class OBJECT_OT_render_to_viewport_visibility(bpy.types.Operator):
    """SimpleVisibility"""
    bl_idname = "object.render_to_viewport_visibility"
    bl_label = "SimpleVisibility"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        for obj in bpy.data.objects:
            obj.hide_render =  obj.hide_get()
            obj.hide_viewport = False

        return {'FINISHED'}


class OBJECT_MT_outliner_set_menu(bpy.types.Menu):
    bl_label = "SimpleVisibility"
    bl_idname = "object.render_to_viewport_visibility_menu"
    
    def draw(self, context):
        addon_prefs = bpy.context.preferences.addons[__name__].preferences
        layout = self.layout
        layout.separator()
        layout.label(text="Operators")
        layout.operator("object.render_to_viewport_visibility", text="Set Render To Viewport Vis.",
                        icon='UV_SYNC_SELECT')
        layout.separator()
        layout.label(text="Preferences")
        layout.prop(addon_prefs, "autoUpdate",text="AutoUpdate")
     
class SimpleVisibility_Preferences(AddonPreferences):
    bl_idname = __name__

    autoUpdate: BoolProperty(
        name="AutoUpdate Visibility Settings before Render",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="The visibility icon update can be triggered manually in the outliner context menu, but there is also an optional AutoUpdate mechanism.")
        layout.prop(self, "autoUpdate")


     
def menu_obj(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("object.render_to_viewport_visibility_menu")

@persistent
def on_before_render(scene):
    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    if addon_prefs.autoUpdate:
        for obj in bpy.data.objects:
            obj.hide_render =  obj.hide_get()
            obj.hide_viewport = False
 
 
def register():

    bpy.utils.register_class(OBJECT_MT_outliner_set_menu)
    bpy.utils.register_class(OBJECT_OT_render_to_viewport_visibility)
    bpy.utils.register_class(SimpleVisibility_Preferences)
    bpy.types.OUTLINER_MT_context_menu.append(menu_obj)  
    bpy.app.handlers.render_pre.append(on_before_render)


def unregister():
    bpy.app.handlers.render_pre.remove(on_before_render)
    bpy.types.OUTLINER_MT_context_menu.remove(menu_obj) 
    bpy.utils.unregister_class(SimpleVisibility_Preferences)
    bpy.utils.unregister_class(OBJECT_MT_outliner_set_menu)
    bpy.utils.unregister_class(OBJECT_OT_render_to_viewport_visibility)


    
if __name__ == "__main__":
    register()