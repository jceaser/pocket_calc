import unittest
from PocketCalc import AppLogic

#DOWN=u'\u2193'  # down arrow
#DIVIDE=u'\u00f7'    #divide symbol
POW10="10"+u'\u02E3'
POW="y"+u'\u02E3'
SQUARE=u'\u221A'+'x'
ROOT=u'\u221A'+'x'
E="e"+u'\u02E3'
MOD='MOD'


class InputStub:
    def __init__(self):
        self.text = ""
    def get(self):
        return self.text
class ViewStub:
    def __init__(self):
        self.input = InputStub()
        self.stackView = None
    def clearInput(self):
        pass

class TestPocketCalc(unittest.TestCase):

    def unaryWrapper(self, app, input, cmd, result):
        app.stack = [input]
        app.cmdUnaryMath(cmd)
        self.assertEqual(app.stack, result)
    def binaryWrapper(self, app, x, y, cmd, result):
        app.stack = [y, x]
        app.cmdBinaryMath(cmd)
        self.assertEqual(app.stack, result)

    def test_line(self):
        app=AppLogic(ViewStub())

        app.processLine("2 2 +")
        self.assertEqual(app.stack, [4])

        app.stack = []
        app.processLine("2:2 +")
        self.assertEqual(app.stack, [4])

        app.stack = []
        app.processLine("2:2 6:3 +:1 *:3")
        self.assertEqual(app.stack, [288.0])
    
    def test_stack(self):
        app=AppLogic(ViewStub())
        
        app.stack = [1, 2, 3, 4]
        app.cmdRotateLeft()
        self.assertEqual(app.stack, [2, 3, 4, 1])

        app.stack = [1, 2, 3, 4]
        app.cmdRotateRight()
        self.assertEqual(app.stack, [4, 1, 2, 3])

        app.stack = [1, 2, 3, 4]
        app.cmdSwapTop2()
        self.assertEqual(app.stack, [1, 2, 4, 3])

        app.stack = [1, 2, 3, 4]
        app.cmdDropTop()
        self.assertEqual(app.stack, [1, 2, 3])        
    
    def test_basic(self):
        app=AppLogic(ViewStub())
        app.stack = [1, 2]
        app.cmdPlus()
        self.assertEqual(app.stack, [3.0])
        
        app.stack = [1, 2]
        app.cmdMinus()
        self.assertEqual(app.stack, [-1.0])
        
        app.stack = [1, 2]
        app.cmdTimes()
        self.assertEqual(app.stack, [2.0])
        
        app.stack = [1, 2]
        app.cmdDiv()
        self.assertEqual(app.stack, [0.5])

    def test_average(self):
        app=AppLogic(ViewStub())
        app.stack = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        app.cmdAvg()
        self.assertEqual(app.stack, [4.0])
    def test_standard_deviation(self):
        app=AppLogic(ViewStub())
        app.stack = [10, 12, 23, 23, 16, 23, 21, 16]
        app.cmdStandardDeviation()
        self.assertEqual(app.stack, [4.898979485566356])

    def test_unary_math(self):
        app=AppLogic(ViewStub())
        self.unaryWrapper(app, 3.14, E, [23.103866858722185])
        self.unaryWrapper(app, 3.14, "log", [1.144222799920162])
        self.unaryWrapper(app, 3.14, ROOT, [1.772004514666935])
        self.unaryWrapper(app, 3.14, "log2", [1.6507645591169022])
        self.unaryWrapper(app, 3.14, "log10", [0.49692964807321494])
        self.unaryWrapper(app, 3.14, POW10, [1380.3842646028852])
        #self.unaryWrapper(app, 3.14, POW, [9.8596])
        self.unaryWrapper(app, 3.14, "1/x", [0.3184713375796178])
        self.unaryWrapper(app, 3.14, "sin", [0.05477590985343363])
        self.unaryWrapper(app, 3.14, "cos", [0.998498672858271])
        self.unaryWrapper(app, 3.14, "tan", [0.054858270063227854])
    def test_binary_math(self):
        app=AppLogic(ViewStub())
        self.binaryWrapper(app, 2, 3, POW, [9.0])
        self.binaryWrapper(app, 2, 3, MOD, [1])
def main():
    unittest.main()

if __name__ == "__main__":
    main()
