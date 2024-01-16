import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

def create_image(width, height, color1, color2):
    # Funkcja do tworzenia ikony dla pystray
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [width // 4, height/4, width*2/4, height],
        fill=color2)
    

    return image

def setup_tray_icon(root, icon_title, icon_tooltip):
    def on_show_window(icon, item):
        icon.stop()
        root.after(0, root.deiconify)  # Pokaż okno

    def on_exit(icon, item):
        icon.stop()
        root.destroy()  # Zamknij aplikację

    def hide_window():
        root.withdraw()  # Ukryj okno
        image = create_image(64, 64, 'white', '#2B70E4')
        menu = (item('Pokaż', on_show_window), item('Wyjdź', on_exit))
        icon = pystray.Icon(icon_title, image, icon_tooltip, menu)
        icon.run()

    return hide_window
