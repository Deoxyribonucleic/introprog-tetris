class Block:
    def __init__(self, block_type, xpos=0, ypos=0):
        self.shape = block_type["shape"]
        self.representation = block_type["representation"]
        self.xpos = xpos
        self.ypos = ypos

    def rotate(self):
        self.shape = [[e[len(self.shape[0])-1-i] for e in self.shape] for i in range(len(self.shape[0]))]

blocks = [
    {
        "shape": 
        [
            [1],
            [1],
            [1],
            [1]
        ],
        "representation": 'I'
    },
    {
        "shape":
        [
            [1,0],
            [1,1],
            [1,0]
        ],
        "representation": 'T'
    },
    {
        "shape":
        [
            [1,1],
            [1,1]
        ],
        "representation": 'O'
    },
    {
        "shape":
        [
            [1,0],
            [1,0],
            [1,1]
        ],
        "representation": 'L'
    },
    {
        "shape":
        [
            [0,1],
            [0,1],
            [1,1]
        ],
        "representation": 'J'
    }
]
