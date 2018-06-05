import tornado.ioloop
import tornado.web
import argparse
import os
datadir = 'data/distributed'

parser = argparse.ArgumentParser(description="mcts self play script") 
parser.add_argument('--verbose', '-v', help='verbose mode',type=bool,default=False)
parser.add_argument('--datadir', '-d' ,type=str,help="data dir to store chess plays",default=datadir)
args = parser.parse_args()
datadir = args.datadir


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("OK")

class ChessSubmitHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument("name") 
        content = self.get_argument("content") 
        print("receive {}".format(name))
        if args.verbose == True:
            print(name,content)
        with open(os.path.join(datadir,name),'w',encoding='utf-8') as whdl:
            whdl.write(content)
        self.write("OK")

class BestWeightNameHandler(tornado.web.RequestHandler):
    def get(self):
        filelist = os.listdir('data/prepare_weight')
        filelist = [i[:-6] for i in filelist if '.index' in i]
        self.write(sorted(filelist)[-1])

class ModelGetHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name") 
        model_f = self.get_argument("model_f") 
        file_name = os.path.join('data/prepare_weight/',"{}.{}".format(name,model_f))
        self.set_header("Content-Type",'application/octet-stream')
        self.set_header('Content-Disposition','attachment; filename={}'.format("{}.{}".format(name,model_f)))
        with open(file_name,'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break;
                self.write(data)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/test", TestHandler),
        (r"/submit_chess", ChessSubmitHandler),
        (r"/best_weight", BestWeightNameHandler),
        (r"/model_get", ModelGetHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(10087)
    tornado.ioloop.IOLoop.current().start()