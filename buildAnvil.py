
# Minimal Panel UI for creating an `anvil` object
import panel as pn
pn.extension()

import json
import os
from SEEmeta import anvil

save_directory = pn.widgets.TextInput(
    name="Save Directory",
    value="/Users/66j/Documents/ORNL/code/SEEMeta/"
)

# Allowed values per type
type_options = ["polycrystalline", "single-crystal"]
material_map = {
    "polycrystalline": ["ZTA", "WC", "sintered diamond", "CBN"],
    "single-crystal": ["diamond"]
}
geometry_map = {
    "polycrystalline": ["single toroid", "double toroid", "bridgman"],
    "single-crystal": ["flat","bevelled"]
}
model_map = {
    "polycrystalline": ["standard", "3mm dimple", "other"],
    "single-crystal": ["conical", "flat", "other"]
}
culetDiameter_map = {
    "polycrystalline": 15.55,
    "single-crystal": 1.0
}

# Widgets
anvil_type = pn.widgets.Select(name="Type", options=type_options, value="polycrystalline")

anvil_material = pn.widgets.Select(name="Material")
anvil_culetGeometry = pn.widgets.Select(name="Culet Geometry")
anvil_model = pn.widgets.Select(name="Model")
anvil_culetDiameter = pn.widgets.FloatInput(name="Culet Diameter (mm)")
anvil_stringDescriptor = pn.widgets.StaticText(name="String Descriptor",value="")
debug_output = pn.pane.Markdown("")

# Optional fields
anvil_cadFile = pn.widgets.TextInput(name="CAD File (path)", placeholder="optional")
anvil_manufacturer = pn.widgets.TextInput(name="Manufacturer", placeholder="optional")
anvil_comment = pn.widgets.TextAreaInput(name="Comment", placeholder="optional")

# Update dependent options when type changes
@pn.depends(anvil_type.param.value, watch=True)
def update_dependent_fields(tval):
    m_options = material_map.get(tval, [])
    g_options = geometry_map.get(tval, [])
    model_options = model_map.get(tval, [])
    default_diameter = culetDiameter_map.get(tval, 10.0)

    anvil_material.options = m_options
    anvil_material.value = m_options[0] if m_options else None

    anvil_culetGeometry.options = g_options
    anvil_culetGeometry.value = g_options[0] if g_options else None

    anvil_model.options = model_options
    anvil_model.value = model_options[0] if model_options else None

    # Only update diameter if it's still 0.0
    # if anvil_culetDiameter.value in (0.0, None):
    anvil_culetDiameter.value = default_diameter
    print("[DEBUG]", type(anvil_culetDiameter), anvil_culetDiameter.value)      

def init_defaults():
    update_dependent_fields(anvil_type.value)
    create_anvil(None)

pn.state.onload(init_defaults)

# Output panel
output = pn.pane.JSON(name="Anvil JSON", depth=2, theme="light")

# Create button
create_button = pn.widgets.Button(name="Create Anvil", button_type="primary")

@pn.depends(
    anvil_type.param.value,
    anvil_material.param.value,
    anvil_culetGeometry.param.value,
    anvil_model.param.value,
    anvil_culetDiameter.param.value,
    anvil_cadFile.param.value,
    anvil_manufacturer.param.value,
    anvil_comment.param.value,
    watch=True,
)
def update_anvil_output(*_):
    try:
        anv = anvil(
            type=anvil_type.value,
            material=anvil_material.value,
            culetGeometry=anvil_culetGeometry.value,
            culetDiameter=float(anvil_culetDiameter.value),
            model=anvil_model.value,
        )
        user_cad = anvil_cadFile.value.strip()
        if user_cad:
            anv.cadFile = user_cad
            if user_cad[-4:] != ".cad":
                user_cad = f"{user_cad}.cad"
        anv.manufacturer = anvil_manufacturer.value
        anv.comment = anvil_comment.value
        output.object = anv.to_dict()
        # Also update filename for save
        filename = anv.stringDescriptor or "anvil"
        save_output.filename = f"{filename}.json"
    except Exception as e:
        output.object = {"error": str(e)}

def build_anvil():
    return anvil(
        type=anvil_type.value,
        material=anvil_material.value,
        culetGeometry=anvil_culetGeometry.value,
        culetDiameter=float(anvil_culetDiameter.value),
        model=anvil_model.value,
    )

def create_anvil(event):
    try:
        anv = build_anvil()
        print(f"descriptor is: {anv.stringDescriptor}")
        anv.cadFile = anvil_cadFile.value
        anv.manufacturer = anvil_manufacturer.value
        anv.comment = anvil_comment.value
        output.object = anv.to_dict()
    except Exception as e:
        output.object = {"error": str(e)}

create_button.on_click(create_anvil)

# Save and Load buttons
save_button = pn.widgets.Button(name="Save Anvil to JSON", button_type="success")
load_button = pn.widgets.FileInput(accept=".json")

@pn.depends(load_button.param.value, watch=True)
def load_anvil_from_file(file_bytes):
    if file_bytes is not None:
        try:
            data = json.loads(file_bytes.decode())
            anvil_type.value = data["type"]  # triggers dependent updates
            anvil_material.value = data["material"]
            anvil_culetGeometry.value = data["culetGeometry"]
            anvil_model.value = data.get("model", "")
            anvil_culetDiameter.value = float(data["culetDiameter"])
            anvil_cadFile.value = data.get("cadFile", "")
            anvil_manufacturer.value = data.get("manufacturer", "")
            anvil_comment.value = data.get("comment", "")
        except Exception as e:
            output.object = {"error": f"Failed to load JSON: {e}"}

save_output = pn.widgets.FileDownload(filename="anvil.json", button_type="success", name="Download JSON")

save_status = pn.pane.Markdown("")  # displays success/failure

def save_json(event):
    
    anv = build_anvil()
    debug_output.object = f"stringDescriptor: {anv.stringDescriptor!r}"

    try:
        # anv = build_anvil()
        debug_output.object = f"stringDescriptor: {anv.stringDescriptor!r}"
        anv.cadFile = anvil_cadFile.value
        anv.manufacturer = anvil_manufacturer.value
        anv.comment = anvil_comment.value
        json_str = json.dumps(anv.to_dict(), indent=2)

        filename = f"{anv.stringDescriptor or 'anvil'}.json"
        directory = save_directory.value.strip()
        if not directory:
            raise ValueError("Please specify a save directory.")
        full_path = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(json_str)
        save_status.object = f"✅ Saved to `{full_path}`"
    except Exception as e:
        save_status.object = f"❌ Save failed: {e}"


save_button.on_click(save_json)
pn.Row(create_button, save_button, load_button),

# Layout
ui = pn.Column(
    pn.pane.Markdown("## Create an Anvil"),
    anvil_type,
    anvil_material,
    anvil_culetGeometry,
    anvil_model,
    anvil_culetDiameter,
    anvil_cadFile,
    anvil_manufacturer,
    anvil_comment,
    pn.Row(save_button, load_button),
    save_directory,
    save_status,
    output,
)

ui.servable()

