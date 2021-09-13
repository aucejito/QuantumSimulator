from Gate import Gate
import gates as gt
from PIL import Image, ImageDraw, ImageFont

class Util():
    def loadGateData(gate):
        gate = gate.lower()
        data = gt.gates.get(gate)
        return data

    def generateGateImage(gate : Gate):
        myFont = ImageFont.truetype("images/Myriad Pro Regular.ttf", 250)
        path = 'C:/Users/cargalau/Documents/GitHub/QuantumSimulator/images/customGates/' + gate.symbol + '.jpg'
        
        H, L = (500,500) #Dimensiones de la imagen
        img = Image.new('RGB', (H,L), color='white') #Se crea el objeto Image
        d = ImageDraw.Draw(img) #Permitimos dibujar en la imagen
        w, h = d.textsize(gate.symbol, font=myFont) #Tamaño del texto
        d.text(((H-w)/2,(L-h)/2), gate.symbol, font=myFont, fill="black") #Se añade el texto en el centro
        gate.path_to_img = path #Se guarda la ruta de la imagen en el objeto
        img.save(path) #Generamos la imagen en la ruta especificada
        return path

