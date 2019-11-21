import cv2
import numpy as np
from openvino.inference_engine import IENetwork, IEPlugin


model_xml = 'MobileNetSSD_birds_soja.xml'
model_bin = os.path.splitext(model_xml)[0] + ".bin"

device = 'MYRIAD' #CPU, GPU, FPGA or MYRIAD
plugin_dir = None


plugin = IEPlugin(device=device, plugin_dirs=plugin_dir)

exec_net = IENetwork(model=model_xml, weights=model_bin)


if plugin.device == "CPU":
    supported_layers = plugin.get_supported_layers(net)
    not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
    if len(not_supported_layers) != 0:
        log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                  format(plugin.device, ', '.join(not_supported_layers)))
        log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                  "or --cpu_extension command line argument")
        sys.exit(1)

        
net = plugin.load(network=exec_net)  
detections = net.infer({'data': blob})['detection_out']

# then we can replace the "detections" object with the one we had before in the Run.py...
