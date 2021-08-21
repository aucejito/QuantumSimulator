from Gate import Gate
import gates as gt
from PIL import Image, ImageDraw, ImageFont

class Util():
    def loadGateData(gate):
        gate = gate.lower()
        data = gt.gates.get(gate)
        return data

    def generateGateImage(gate : Gate):
        H, L = (500,500)
        img = Image.new('RGB', (H,L), color='white')
        myFont = ImageFont.truetype("images/Myriad Pro Regular.ttf", 250)
        d = ImageDraw.Draw(img)
        w, h = d.textsize(gate.symbol, font=myFont)
        d.text(((H-w)/2,(L-h)/2), gate.symbol, font=myFont, fill="black")
        path = 'C:/Users/cargalau/Documents/GitHub/QuantumSimulator/images/customGates/' + gate.symbol + '.jpg'
        gate.path_to_img = path
        img.save(path)
        return path

