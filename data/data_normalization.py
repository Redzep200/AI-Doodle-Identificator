import numpy as np
import matplotlib.pyplot as plt

ANT = 1
COMPUTER = 2
COOKIE = 3
HEADPHONES = 4
LIGHTNING = 5


class Data:
    def __init__(self, drawing, label):
        self.drawing = drawing
        self.label = label

    def normalize(self):
        # Convert the drawing to float32 before normalization
        self.drawing = self.drawing.astype('float32')
        self.drawing /= 255.0

def load_dataset(path):
    data = np.load(path)
    return data


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

    # Create a list of Data instances
    ant_dataset = [Data(drawing, label) for drawing, label in zip(ant_drawings, ant_labels)]
    computer_dataset = [Data(drawing, label) for drawing, label in zip(computer_drawings, computer_labels)]
    cookie_dataset = [Data(drawing, label) for drawing, label in zip(cookie_drawings, cookie_labels)]
    headphones_dataset = [Data(drawing, label) for drawing, label in zip(headphones_drawings, headphones_labels)]
    lightning_dataset = [Data(drawing, label) for drawing, label in zip(lightning_drawings, lightning_labels)]

    # Normalize each drawing
    for sample in ant_dataset:
        sample.normalize()

    for sample in computer_dataset:
        sample.normalize()

    for sample in cookie_dataset:
        sample.normalize()

    for sample in headphones_dataset:
        sample.normalize()

    for sample in lightning_dataset:
        sample.normalize()


    # Combine all datasets into a single list
    dataset = []

    # Extend the list with each dataset
    dataset.extend(ant_dataset)
    dataset.extend(computer_dataset)
    dataset.extend(cookie_dataset)
    dataset.extend(headphones_dataset)
    dataset.extend(lightning_dataset)

    # Shuffle the combined dataset
    np.random.shuffle(dataset)


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
        sample = dataset[i]
        first_drawing = sample.drawing.reshape((28, 28))
        label = GetLabel(sample.label)

        plt.imshow(first_drawing, cmap='gray')
        plt.title(f'Label: {label}')
        plt.show()

        print(f"Drawing array: {sample.drawing}\n Label: {label}\n")
