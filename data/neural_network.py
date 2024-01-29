from .data_normalization import LOAD_DATA #za pokretanje iz canvas.py dodati tacku
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, random_split
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import matplotlib.pyplot as plt
from torchvision import transforms

print('Loading data...')
dataset = LOAD_DATA()

transform_train = transforms.Compose([
    transforms.RandomRotation(degrees=30),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ColorJitter(brightness=0.1, contrast=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.3, 0.3)),  # Adding image shift
    transforms.ToTensor(),
])

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

train_data, test_data = random_split(dataset, [train_size, test_size])

# Apply transformations to the training dataset
train_data.dataset.transform = transform_train

# train_data, test_data = train_test_split(dataset, test_size=0.2, transform=transform_train)
print('\nDataset: ' + str(len(dataset)) + '\nTrain data: ' + str(len(train_data)) + '\nTest data: ' + str(len(test_data)))

loaders = {
    
    'train': DataLoader(train_data,
                        batch_size=100,
                        shuffle=False,
                        num_workers=1),
    
    'test': DataLoader(test_data,
                       batch_size=100,
                       shuffle=False,
                       num_workers=1)
}






class CNN(nn.Module):
    
    def __init__ (self):
        super(CNN, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 5)
    
    def forward(self, x):
        x = x.view(-1, 1, 28, 28)
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        
        return F.softmax(x,dim=1)
        

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = CNN().to(device)

optimizer = optim.Adam(model.parameters(), lr=0.001)

loss_fn = nn.CrossEntropyLoss()

def train(epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(loaders['train']):
        data, target= data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        target = target.long()
        loss = loss_fn(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 20 == 0:
            print(f'Train epoch: {epoch} [{batch_idx * len(data)}/{len(loaders["train"].dataset)} ({100. * batch_idx / len(loaders["train"]):.0f}%)]\t{loss.item():.6f}')
            
            
def test():
    model.eval()
    
    test_loss = 0
    correct = 0
    
    with torch.no_grad():
        for data, target in loaders['test']:
            data, target = data.to(device), target.to(device)
            target = target.long()
            output = model(data)
            test_loss += loss_fn(output, target).item()
            pred = output.argmax(dim = 1, keepdim = True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            
    test_loss /= len((loaders["test"]).dataset)
    print(f'\nTest set, average loss: {test_loss:.4f}, Accuracy: {correct}/{len(loaders["test"].dataset)} ({100. * correct / len(loaders["test"].dataset):.2f})%\n')
            

if __name__ == '__main__':
    for epoch_num in range(1,6):
        train(epoch_num)
        test()
    torch.save(model.state_dict(),'doodle_identificator.pth')
    