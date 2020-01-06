#a typical 3D pixel shuffle layer for pytorch
class PixelUpsampler3D(nn.Module):
    def __init__(self,
                 upscaleFactor,
                 # conv=default_conv3d,
                 # n_feats=32,
                 # kernel_size=3,
                 # bias=True
                 ):
        super(PixelUpsampler3D, self).__init__()
        self.scaleFactor = upscaleFactor

    def PixelShuffle(self, input, upscaleFactor):
        batchSize, channels, inDepth, inHeight, inWidth = input.size()
        channels //= upscaleFactor[0] * upscaleFactor[1] * upscaleFactor[2]
        outDepth = inDepth * upscaleFactor[0]
        outHeight = inHeight * upscaleFactor[1]
        outWidth = inWidth * upscaleFactor[2]
        inputView = input.contiguous().view(
            batchSize, channels, upscaleFactor[0], upscaleFactor[1], upscaleFactor[2], inDepth,
            inHeight, inWidth)
        shuffleOut = inputView.permute(0, 1, 5, 2, 6, 3, 7, 4).contiguous()
        return shuffleOut.view(batchSize, channels, outDepth, outHeight, outWidth)

    def forward(self, x):
        # x = self.conv(x)
        up = self.PixelShuffle(x, self.scaleFactor)
        return up
