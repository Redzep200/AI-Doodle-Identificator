import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset


ANT = 1
COMPUTER = 2
COOKIE = 3
HEADPHONES = 4
LIGHTNING = 5


class Data(Dataset):
    def __init__(self, drawing, label):
        self.drawing = drawing 
        self.label = label 

    def __len__(self):
        return len(self.drawing)

    def __getitem__(self, idx):
        return self.drawing[idx], self.label[idx]
        
        

def normalize(data):
    normalized = data.astype('float32')
    normalized /= 255.0
    return normalized

def load_dataset(path):
    data = np.load(path)
    normalized_data = normalize(data)
    return normalized_data



def LOAD_DATA():
    # Load the dataset
    ant_path = 'ant.npy'
    computer_path='computer.npy'
    cookie_path='cookie.npy'
    headphones_path='headphones.npy'
    lightning_path='lightning.npy'

    # Save the drawings into a object
    ant_drawings = load_dataset(ant_path)
    computer_drawings = load_dataset(computer_path)
    cookie_drawings = load_dataset(cookie_path)
    headphones_drawings = load_dataset(headphones_path)
    lightning_drawings = load_dataset(lightning_path)

    # Create an array of labels matching the number of drawings
    ant_labels = np.full(len(ant_drawings), fill_value=ANT) 
    computer_labels = np.full(len(computer_drawings), fill_value=COMPUTER) 
    cookie_labels = np.full(len(cookie_drawings), fill_value=COOKIE) 
    headphones_labels = np.full(len(headphones_drawings), fill_value=HEADPHONES) 
    lightning_labels = np.full(len(lightning_drawings), fill_value=LIGHTNING) 

    junk_data = []
    junk_data.extend(ant_drawings)
    junk_data.extend(computer_drawings)
    junk_data.extend(cookie_drawings)
    junk_data.extend(headphones_drawings)
    junk_data.extend(lightning_drawings)

    junk_labels=[]
    junk_labels.extend(ant_labels)
    junk_labels.extend(computer_labels)
    junk_labels.extend(cookie_labels)
    junk_labels.extend(headphones_labels)
    junk_labels.extend(lightning_labels)

    junk_data= np.array(junk_data)
    junk_labels= np.array(junk_labels)

    indices = np.arange(len(junk_data))
    np.random.shuffle(indices)

    shuffled_data = junk_data[indices]
    shuffled_labels = junk_labels[indices]


    dataset = Data(shuffled_data,shuffled_labels)

    


    return dataset


def GetLabel(label):

    def case1():
        return "Ant"

    def case2():
        return "Computer"

    def case3():
        return "Cookie"

    def case4():
        return "Headphones"

    def case5():
        return "Lightning"

    def default():
        return "Not Applicable"

    # Look up the case function from the dictionary
    selected_case = {
        1: case1,
        2: case2,
        3: case3,
        4: case4,
        5: case5
    }.get(label, default)

    # Call the selected function and return its result
    return selected_case()




if __name__ == "__main__":
    dataset = LOAD_DATA()

    for i in range(5):
        drawing, label =  dataset[i]

        first_drawing = drawing.reshape((28, 28))
        # label = GetLabel(label)

        plt.imshow(first_drawing, cmap='gray')
        plt.title(f'Label: {label}')
        plt.show()

        print(f"Drawing array: {drawing}\n Label: {label}\n")
