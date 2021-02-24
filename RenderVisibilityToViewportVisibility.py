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
from bpy.types import Operator

bl_info = {
    "name": "Render Visibility To Viewport Visibility",
    "description": "Set all objects render-visibility to viewport-visibility",
    "author": "Debuk",
    "version": (1, 0, 0),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Object"    
}


class OBJECT_OT_RenderToViewportVisibility(bpy.types.Operator):
    """Render To Viewport Visibility"""
    bl_idname = "object.render_to_viewport_visibility"
    bl_label = "Render Visibility To Viewport Visibility"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        for obj in bpy.data.objects:
            obj.hide_render =  obj.hide_get()
            obj.hide_viewport = obj.hide_get()

        return {'FINISHED'}


class OBJECT_MT_outliner_set_menu(bpy.types.Menu):
    bl_label = "Render Vis."
    bl_idname = "object.render_to_viewport_visibility_menu"
    
    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.operator("object.render_to_viewport_visibility", text="Set Render To Viewport Vis.",
                        icon='UV_SYNC_SELECT')
                        
def menu_obj(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("object.render_to_viewport_visibility_menu")


def register():
    bpy.utils.register_class(OBJECT_MT_outliner_set_menu)
    bpy.utils.register_class(OBJECT_OT_RenderToViewportVisibility)
    bpy.types.OUTLINER_MT_context_menu.append(menu_obj)  

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RenderToViewportVisibility)
    bpy.utils.unregister_class(OBJECT_MT_outliner_set_menu)
    bpy.types.OUTLINER_MT_context_menu.remove(menu_obj) 
    
if __name__ == "__main__":
    register()