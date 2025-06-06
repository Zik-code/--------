import torch
import torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000,init_weights = False):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            # 第一层卷积层 ,原out_channel为96，这里为了减少计算量，设置为48
            # 后面的卷积核个数相较原来的网络结构都减半
            nn.Conv2d(1, 48, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            # 第二层卷积层
            nn.Conv2d(48, 128, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            # 第三层卷积层
            nn.Conv2d(128, 192, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            # 第四层卷积层
            nn.Conv2d(192, 192, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            # 第五层卷积层
            nn.Conv2d(192, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.classifier = nn.Sequential(
            # Dropout防止过拟合,p为失活比例
            nn.Dropout(p=0.5),
            # 第六层全连接层
            nn.Linear(128 * 6 * 6, 2048),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            # 第七层全连接层
            nn.Linear(2048, 2048),
            nn.ReLU(inplace=True),
            # 第八层全连接层
            nn.Linear(2048, num_classes),
        )
        if init_weights:
            self._initialize_weights()
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, start_dim = 1)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m,nn.Conv2d):
                nn.init.kaiming_normal_(m.weight,mode= 'fan_out',)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
                elif isinstance(m,nn.Linear):
                    nn.init.normal_(m.weight , 0, 0.01)
                    nn.init.constant_(m.bias,0)



# 测试代码
if __name__ == "__main__":
    model = AlexNet()
    input_tensor = torch.randn(1, 3, 224, 224)
    output = model(input_tensor)
    print(output.shape)