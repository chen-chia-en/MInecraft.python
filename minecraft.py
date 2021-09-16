from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound.wav',loop = False, autoplay = False)


window.fps_counter.enabled = False
window.exit_button.visible = False

block_pick = 1
def update():
    # 函數內只要沒有「定義」跟外部全域變數相同的區域變數 (local variable) 名稱，就可以直接取得外部全域變數的數值，但不可修改，
    # 修改外部全域變數的值，就要利用關鍵字 global。我們需要修改全域變數 block_pick 因為數值要回傳 input(self,key)去 if-statement中
    global block_pick
    # update function中表達 左右鍵 left/right mouse; Voxel (Button) 中用 'left/right mouse down' 
    if held_keys['left mouse'] or held_keys['right mouse']: 
        hand.active()
    else:
        hand.passive()
    # 指令如果很簡短，可以直接在 : 後面寫出，
    if held_keys['1']:
        block_pick = 1
    if held_keys['2']:
        block_pick = 2
    if held_keys['3']:
        block_pick = 3
    if held_keys['4']:
        block_pick = 4

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture):
        # ???super()
        super().__init__(
            # Button 需要 parent = scene
            parent = scene,
            position = position,
            model = 'assets/block.obj',
            # origin_y = 0.5起始點離地面0.5。 很重要 會影響create cube 的靈敏度 
            origin_y = 0.5,
            texture = texture,
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 0.5
            )

    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                # mouse.normal 就是會偵測key hover 的表面去新增物件，也就是「原有位置 + mouse.normal 位置」。print(mouse.normal) >> (0,0,1)、(-1,0,0)....
                if block_pick == 1:
                    Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2:
                    Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3:
                    Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4:
                    Voxel(position = self.position + mouse.normal, texture = dirt_texture)
            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True)

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm.obj',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-25,0),
            position = Vec2(0.7,-0.6))

    def active(self):
        self.position = Vec2(0.6,-0.5)

    def passive(self):
        self.position = Vec2(0.7,-0.6)

for z in range(30):
    for x in range(30):
        voxel = Voxel(position = (x,0,z))

FirstPersonController()
Sky()
hand = Hand()
# class Hand()先建立instance 存進變數hand，再呼叫class中的方法 hand.active()
app.run()

