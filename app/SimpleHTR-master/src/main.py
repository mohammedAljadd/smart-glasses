import json
from typing import Tuple, List

import cv2
import editdistance


from dataloader_iam import DataLoaderIAM, Batch
from model import Model, DecoderType
from preprocessor import Preprocessor


class FilePaths:
    """Filenames and paths to data."""
    fn_char_list = 'C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/model/charList.txt'
    fn_summary = 'C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/model/summary.json'
    fn_corpus = 'C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/model/corpus.txt'


def get_img_height() -> int:
    """Fixed height for NN."""
    return 32


def get_img_size(line_mode: bool = False) -> Tuple[int, int]:
    """Height is fixed for NN, width is set according to training mode (single words or text lines)."""
    if line_mode:
        return 256, get_img_height()
    return 128, get_img_height()


def write_summary(char_error_rates: List[float], word_accuracies: List[float]) -> None:
    """Writes training summary file for NN."""
    with open(FilePaths.fn_summary, 'w') as f:
        json.dump({'charErrorRates': char_error_rates, 'wordAccuracies': word_accuracies}, f)


def char_list_from_file() -> List[str]:
    with open(FilePaths.fn_char_list) as f:
        return list(f.read())


from path import Path
def infer(model: Model, fn_img: Path, img) -> None:
    """Recognizes text in image provided by file path."""
    
    assert img is not None

    preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
    img = preprocessor.process_img(img)

    batch = Batch([img], None, 1)
    recognized, probability = model.infer_batch(batch, True)
    #print(f'Recognized: "{recognized[0]}"')
    #print(f'Probability: {probability[0]}')

    return recognized[0]

'''
def parse_args() -> argparse.Namespace:
    """Parses arguments from the command line."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', choices=['train', 'validate', 'infer'], default='infer')
    parser.add_argument('--decoder', choices=['bestpath', 'beamsearch', 'wordbeamsearch'], default='bestpath')
    parser.add_argument('--batch_size', help='Batch size.', type=int, default=100)
    parser.add_argument('--data_dir', help='Directory containing IAM dataset.', type=Path, required=False)
    parser.add_argument('--fast', help='Load samples from LMDB.', action='store_true')
    parser.add_argument('--line_mode', help='Train to read text lines instead of single words.', action='store_true')
    parser.add_argument('--img_file', help='Image used for inference.', type=Path, default='C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/data/coda.jpg')
    parser.add_argument('--early_stopping', help='Early stopping epochs.', type=int, default=25)
    parser.add_argument('--dump', help='Dump output of NN to CSV file(s).', action='store_true')

    return parser.parse_args()
'''
def main():
    """Main function."""
    import json
    from typing import Tuple, List

    import cv2
    import editdistance


    from dataloader_iam import DataLoaderIAM, Batch
    from model import Model, DecoderType
    from preprocessor import Preprocessor


    class FilePaths:
        """Filenames and paths to data."""
        fn_char_list = 'C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/model/charList.txt'
        fn_summary = 'C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/model/summary.json'
        fn_corpus = 'C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/model/corpus.txt'


    def get_img_height() -> int:
        """Fixed height for NN."""
        return 32


    def get_img_size(line_mode: bool = False) -> Tuple[int, int]:
        """Height is fixed for NN, width is set according to training mode (single words or text lines)."""
        if line_mode:
            return 256, get_img_height()
        return 128, get_img_height()


    def write_summary(char_error_rates: List[float], word_accuracies: List[float]) -> None:
        """Writes training summary file for NN."""
        with open(FilePaths.fn_summary, 'w') as f:
            json.dump({'charErrorRates': char_error_rates, 'wordAccuracies': word_accuracies}, f)


    def char_list_from_file() -> List[str]:
        with open(FilePaths.fn_char_list) as f:
            return list(f.read())


    from path import Path
    def infer(model: Model, fn_img: Path, img) -> None:
        """Recognizes text in image provided by file path."""
        
        assert img is not None

        preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
        img = preprocessor.process_img(img)

        batch = Batch([img], None, 1)
        recognized, probability = model.infer_batch(batch, True)
        #print(f'Recognized: "{recognized[0]}"')
        #print(f'Probability: {probability[0]}')

        return recognized[0]

    '''
    def parse_args() -> argparse.Namespace:
        """Parses arguments from the command line."""
        parser = argparse.ArgumentParser()

        parser.add_argument('--mode', choices=['train', 'validate', 'infer'], default='infer')
        parser.add_argument('--decoder', choices=['bestpath', 'beamsearch', 'wordbeamsearch'], default='bestpath')
        parser.add_argument('--batch_size', help='Batch size.', type=int, default=100)
        parser.add_argument('--data_dir', help='Directory containing IAM dataset.', type=Path, required=False)
        parser.add_argument('--fast', help='Load samples from LMDB.', action='store_true')
        parser.add_argument('--line_mode', help='Train to read text lines instead of single words.', action='store_true')
        parser.add_argument('--img_file', help='Image used for inference.', type=Path, default='C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/data/coda.jpg')
        parser.add_argument('--early_stopping', help='Early stopping epochs.', type=int, default=25)
        parser.add_argument('--dump', help='Dump output of NN to CSV file(s).', action='store_true')

        return parser.parse_args()
    '''

    # parse arguments and set CTC decoder
    import argparse
    from path import Path
    import json
    from typing import Tuple, List

    import cv2
    import editdistance


    from dataloader_iam import DataLoaderIAM, Batch
    from model import Model, DecoderType
    from preprocessor import Preprocessor
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', choices=['train', 'validate', 'infer'], default='infer')
    parser.add_argument('--decoder', choices=['bestpath', 'beamsearch', 'wordbeamsearch'], default='bestpath')
    parser.add_argument('--batch_size', help='Batch size.', type=int, default=100)
    parser.add_argument('--data_dir', help='Directory containing IAM dataset.', type=Path, required=False)
    parser.add_argument('--fast', help='Load samples from LMDB.', action='store_true')
    parser.add_argument('--line_mode', help='Train to read text lines instead of single words.', action='store_true')
    parser.add_argument('--img_file', help='Image used for inference.', type=Path, default='C:/Users/install.PO-ETU007/Desktop/SimpleHTR/SimpleHTR-master/data/coda.jpg')
    parser.add_argument('--early_stopping', help='Early stopping epochs.', type=int, default=25)
    parser.add_argument('--dump', help='Dump output of NN to CSV file(s).', action='store_true')
    args = parser.parse_args()
    
    decoder_mapping = {'bestpath': DecoderType.BestPath,
                       'beamsearch': DecoderType.BeamSearch,
                       'wordbeamsearch': DecoderType.WordBeamSearch}
    decoder_type = decoder_mapping[args.decoder]

   

    model = Model(char_list_from_file(), decoder_type, must_restore=True, dump=args.dump)
    
    # Predict all lines:
    import os
    string = ""
    folder_lines = "C:/Users/install.PO-ETU007/Desktop/MyProjects\iEars/app\static\htr_results\lignes"
   
    for img in os.listdir(folder_lines): 
        img_path = os.path.join(folder_lines, img)
        line = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        string += infer(model, args.img_file, cv2.bitwise_not(line))+" "
        
   
    print("Result is:" + str(string))
    with open('C:/Users/install.PO-ETU007/Desktop/MyProjects\iEars/htr_results.txt', 'w') as f:
        f.write(string)

    

main()
