import bpy

debug_mode=False

def get_all_layer_collections(top_level_layer_coll):
    allLayerColls = []
    get_all_layer_collections_internal(top_level_layer_coll, allLayerColls)
    return allLayerColls;
    
def get_all_layer_collections_internal(layercoll, list):
    list.append(layercoll)
    for currCol in layercoll.children:
        get_all_layer_collections_internal(currCol, list)

def get_window_no():
    wm = bpy.context.window_manager
    index =0
    for window in wm.windows:
        if window == bpy.context.window:
            return index
        index +=1
    return -1

def get_window_no_view_layer(no):
    wm = bpy.context.window_manager
    index =0
    for window in wm.windows:
        if (index == no):
            return window.view_layer.name
        index+=1
    return None


def print_window_layer_data():
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("Context layercoll coll:" +repr(bpy.context.layer_collection.collection))
    wm = bpy.context.window_manager
    act_window= bpy.context.window


    print("LayerInfo: --------------------------")
    if act_window != None:
        print("Context Viewlayer" + repr(bpy.context.window.view_layer))
        # Master Collection
        print("Context Viewlayer LC" + repr(bpy.context.window.view_layer.layer_collection.collection.name))
        print("Context Viewlayer AC" + repr(bpy.context.window.view_layer.active_layer_collection.collection.name))
    else:
        print("Window was None")

    windowCount = len(wm.windows)
    print("Windows" + repr(windowCount))

    # Windows List
    index =0
    for window in wm.windows:
        print("Window No:"+ repr(index)+ " ----------------")
        print(window.x)
        print(window.y)
        print(window.width)
        print(window.height)
        print("VL: " + get_window_no_view_layer(index))
        index+=1
    render_vl = get_render_window_vl()
    if render_vl == None:
        print("No RenderWindow found")
    else:
        print("RenderWindow VL:"+render_vl.name)

def get_render_window_vl():
    wm = bpy.context.window_manager
    index =0
    for window in wm.windows:
        scrareas = window.screen.areas
        for area in scrareas:
            if area.type =='IMAGE_EDITOR':
                for space in area.spaces:
                    if space.image.type == "RENDER_RESULT":
                        if debug_mode: print("Window " + repr(index) + " has an image editor showing the render result")
                        return window.view_layer
        index+=1
    return None


def set_obj_hidings_new():

    # This will be None with OnBeforeRender
    act_window= bpy.context.window

    if debug_mode: print_window_layer_data()
    view_layer = None
    view_layer_root_coll = None

    if act_window != None:
        # Non Render Case ##################################
        view_layer =act_window.view_layer
        view_layer_root_coll= view_layer.layer_collection.collection

    else:
        # Render Case ######################################
        render_vl = get_render_window_vl()
        if render_vl == None:
            return False
        else:
            view_layer = render_vl
            view_layer_root_coll = render_vl.layer_collection.collection

    # Set hidings
    obj_count = len(view_layer_root_coll.all_objects)

    i =0
    while (i< obj_count):
        obj = view_layer_root_coll.all_objects[i]
        obj.hide_render = obj.hide_get(view_layer=view_layer)
        obj.hide_viewport = False
        i +=1

    return True


def set_obj_hidings_old():
    # Currently crashes (since 2.93)
    objs = bpy.context.layer_collection.collection.all_objects
    for obj in objs:
        obj.hide_render = obj.hide_get(view_layer=bpy.context.view_layer)
        obj.hide_viewport = False

def set_coll_hidings():
    cols = get_all_layer_collections(bpy.context.layer_collection)
    for col in cols:
        col.collection.hide_viewport = False
        col.collection.hide_render = col.hide_viewport

class OBJECT_OT_set_render_to_viewport_visibility(bpy.types.Operator):
    """SimpleVisibility"""
    bl_idname = "object.set_render_to_viewport_visibility"
    bl_label = "SimpleVisibility"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        set_coll_hidings()
        #set_obj_hidings_old()
        done = set_obj_hidings_new()
        if done: self.report({'INFO'}, "Render To Viewport Visibility done")
        else: self.report({'WARNING'}, "Render To Viewport Visibility failed")
        return {'FINISHED'}


class OBJECT_MT_outliner_set_render_to_viewport_vis_menu(bpy.types.Menu):
    bl_label = "SimpleVisibility"
    bl_idname = "OBJECT_MT_outliner_set_render_to_viewport_vis_menu"
    
    def draw(self, context):
        addon_prefs = bpy.context.preferences.addons["SimpleVisibility"].preferences
        layout = self.layout
        layout.separator()
        layout.label(text="Operators")
        layout.operator("object.set_render_to_viewport_visibility", text="Set Render To Viewport Vis.",
                        icon='UV_SYNC_SELECT')
        layout.separator()
        layout.label(text="Preferences")
        layout.prop(addon_prefs, "auto_sync",text="Auto Sync")

        if (debug_mode):layout.label(text="Window No: " + repr(get_window_no()) + " " + repr(get_window_no_view_layer(get_window_no())))

     
