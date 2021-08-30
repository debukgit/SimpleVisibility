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
from .SimpleVisibility import *
bl_info = {
    "name": "SimpleVisibility",
    "description": "Sets every objects render-visibility to be in sync with viewport-visibility",
    "author": "Debuk",
    "version": (1, 3, 0),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Object"
}


class SimpleVisibility_Preferences(AddonPreferences):
    bl_idname = __name__

    auto_sync: BoolProperty(
        name="AutoSync Visibility Settings before Render",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(
            text="The visibility icon sync can be triggered manually in the outliner context menu, but there is also an optional AutoSync mechanism.")
        layout.prop(self, "auto_sync")


def menu_obj(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("OBJECT_MT_outliner_set_render_to_viewport_vis_menu")


@persistent
def on_before_render(scene):
    addon_prefs = bpy.context.preferences.addons["SimpleVisibility"].preferences
    if addon_prefs.auto_sync:

        cols = get_all_layer_collections(bpy.context.layer_collection)
        for col in cols:
            col.collection.hide_viewport = False
            col.collection.hide_render = col.hide_viewport

        done = set_obj_hidings_new()
        if not done: print(" Auto Sync failed")


def register():
    bpy.utils.register_class(OBJECT_MT_outliner_set_render_to_viewport_vis_menu)
    bpy.utils.register_class(OBJECT_OT_set_render_to_viewport_visibility)
    bpy.utils.register_class(SimpleVisibility_Preferences)
    bpy.types.OUTLINER_MT_context_menu.append(menu_obj)
    bpy.app.handlers.render_pre.append(on_before_render)


def unregister():
    bpy.app.handlers.render_pre.remove(on_before_render)
    bpy.types.OUTLINER_MT_context_menu.remove(menu_obj)
    bpy.utils.unregister_class(SimpleVisibility_Preferences)
    bpy.utils.unregister_class(OBJECT_MT_outliner_set_render_to_viewport_vis_menu)
    bpy.utils.unregister_class(OBJECT_OT_set_render_to_viewport_visibility)


if __name__ == "__main__":
    register()