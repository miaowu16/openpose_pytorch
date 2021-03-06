# coding:utf-8
import torch
from torch.autograd import Variable
import torch.functional as F


#  S=S*,L=L*  --  Loss=S+L

class lossPose(torch.nn.Module):
    """ confidence map loss & part affinity field
    target:
        1) produce part confidence map loss at stage t
    objective Loss:
        f(S,t) = W(P)*L2((St-S*))
        then integral for every points P in an image
        and every parts J
    """

    def __init__(self):
        """
         confidence maps S1 = ρ1 (F)
        """
        super(lossPose, self).__init__()

    def forward(self, predication, wp, sp):
        """
        pre shape: batch * parts * h * w
        wp shape: h*w
        :param predication: containing the confidence map
        :param ground_truth: a tuple
            containing the binary "mask" of people
            ground truth confidence "heatmap"
        :return:
        """
        # wp, sp = ground_truth
        batchs, _, w, h = predication.shape
        mask = Variable(wp).cuda()
        truth = mask * Variable((sp.repeat(1, 6, 1, 1)).cuda())
        try:
            loss_S = (predication - truth) ** 2  # mask *
            return loss_S.sum() / (batchs)  # * w * h
        except Exception as e:
            print('wowo:', e)
            return None


class loss_PAF(torch.nn.Module):
    """ground truth part affinity vector field
        f(L,t) = W(P)*L2((Lt-L*))
        Variable()
    """

    def __init__(self):
        super(loss_PAF, self).__init__()

    def forward(self, prediction, wp, lp):
        """

        :param prediction:
        :param ground_truth: tuple
            containing two dataset:
            binary mask file &
            L ground truth part affinity vector field
        :return:
        """
        # wp, lp = ground_truth
        batchs, _, w, h = prediction.shape
        mask = Variable(wp.expand_as(prediction.data)).cuda()
        loss_L = mask * (prediction - Variable(lp.repeat(1, 6, 1, 1)).cuda()) ** 2

        return loss_L.sum() / (batchs)  # * w * h


'''
class loss(torch.nn.Module):
    """
    final loss function
    """

    def __init__(self):
        super(loss, self).__init__()

    def forward(self, *input):
        """
        input suppose is a list of Variable of scale
        :param input:
        :return:
        """
        loss = sum(input.data)
        return loss


def reshape_as(img, target):
    batch, channel, h, w = target.size()
    _, c_d, h_d, w_d = img.size()

    # $ h & w
    try:
        img = img.data.numpy()
    except:
        img = img.data.cpu().numpy()
    data = data.reshape()
'''
