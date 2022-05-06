import argparse

from src.collect_trainingdata.get_faces_from_camera import TrainingDataCollector
from src.face_embedding.faces_embedding import GenerateFaceEmbedding
from src.training.train_softmax import TrainFaceRecogModel
from src.predictor.facePredictor import FacePredictor


def collectUserImageForRegistration(imageSaveLocation):
    ap = argparse.ArgumentParser()

    ap.add_argument("--faces", default=50,
                    help="Number of faces that camera will get")
    ap.add_argument("--output", default="../datasets/train/" + imageSaveLocation,
                    help="Path to faces output")

    args = vars(ap.parse_args())

    trnngDataCollctrObj = TrainingDataCollector(args)
    trnngDataCollctrObj.collectImagesFromCamera()


def getFaceEmbedding():

    ap = argparse.ArgumentParser()

    ap.add_argument("--dataset", default="../datasets/train",
                    help="Path to training dataset")
    ap.add_argument("--embeddings", default="faceEmbeddingModels/embeddings.pickle")
    # Argument of insightface
    ap.add_argument('--image-size', default='112,112', help='')
    ap.add_argument('--model', default='../insightface/models/model-y1-test2/model,0', help='path to load model.')
    ap.add_argument('--ga-model', default='', help='path to load model.')
    ap.add_argument('--gpu', default=0, type=int, help='gpu id')
    ap.add_argument('--det', default=0, type=int, help='mtcnn option, 1 means using R+O, 0 means detect from begining')
    ap.add_argument('--flip', default=0, type=int, help='whether do lr flip aug')
    ap.add_argument('--threshold', default=1.24, type=float, help='ver dist threshold')
    args = ap.parse_args()

    genFaceEmbdng = GenerateFaceEmbedding(args)
    genFaceEmbdng.genFaceEmbedding()


def trainModel():
    # ============================================= Training Params ====================================================== #

    ap = argparse.ArgumentParser()
    ap.add_argument("--embeddings", default="faceEmbeddingModels/embeddings.pickle",
                    help="path to serialized db of facial embeddings")
    ap.add_argument("--model", default="faceEmbeddingModels/my_model.h5",
                    help="path to output trained model")
    ap.add_argument("--le", default="faceEmbeddingModels/le.pickle",
                    help="path to output label encoder")

    args = vars(ap.parse_args())

    faceRecogModel = TrainFaceRecogModel(args)
    faceRecogModel.trainKerasModelForFaceRecognition()


def makePrediction():
        faceDetector = FacePredictor()
        faceDetector.detectFace()
