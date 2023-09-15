#!/usr/bin/python
# -*- coding: utf8 -*-
"""

@date: 15.09.23
@author: leonhard.hennig@dfki.de
"""
from dataclasses import dataclass

from pytorch_ie.annotations import LabeledSpan
from pytorch_ie.auto import AutoPipeline
from pytorch_ie.core import AnnotationList, annotation_field
from pytorch_ie.documents import TextDocument


@dataclass
class ExampleDocument(TextDocument):
    entities: AnnotationList[LabeledSpan] = annotation_field(target="text")


def predict():
    """Example of inference with trained model.

    It loads pretrained NER model. Then it creates an example document (PyTorch-IE Document) and
    predicts entities from the text in the document.
    """

    documents = [
        ExampleDocument(
            "The most valuable mother-of-pearl is obtained from four species; Pinctada maxima  P. margaritifera  Trochus niloticus and Turbo marmoratus"
        ),
        ExampleDocument(
            "236 BARBICAN. A specimen of this is in the British Museum, and appears to be a young bird in the state of changing its pinnae. 4— BLACK-THROATED BARBICAN. Bucco niger, Indorni. 204. Gm. Lin. 407. Gen. Zoolog. p. 30. Barbu 4 gorge noire de Luon, Son. Voy. 68. t. 34. Buf. vii. p. 103. Black-throated Barbet, Gen. Syn. ii. 501. SOMEWHAT larger and longer than the Common Grosbeak. Bill blackish, furnished with a sort of process or tooth, about two-fifths from the tip ; forehead fine red; the crown, hind part, throat, and neck black ; above each eye a curved stripe of yellow, which, as it proceeds downwards, becomes white, and descends in a strait line to the lower part of the neck; beneath this a black stripe, and between it and the throat a white band, which goes on to, and blends with, the breast ; and this, as well as the rest of the under parts, is white ; middle of the back black, but the side feathers, between the neck and back, have a yellow spot on each ; wing coverts black, four of them fringed with white, and one with yellow, forming a stripe across the wing ; beneath this, some of the feathers are spotted with yellow at the ends ; and under these, others, which have yellow margins ; quills black, bordered with yellow ; legs black. Inhabits the Philippine Islands ; also the Cape of Good Hope. A specimen, from the latter, in the British Museum, was seven inches long, and differed only in having the rump of a beautiful yellow. A. — Bucco niger, Indorni. 204; 8. 3. Le Barbu i Plastron noir, Buf. vii. 104. Bucco rufifrons. Red-fronted Barbet, Gen. Zool. ix. p. 31. Barbu du Cap de B, Esperance, PL enl. 688. 1. Length six inches and a half Bill black; forehead crimson; from this passes a stripe of black over the head, and down the back"
        ),
        ExampleDocument(
            "FISHERY RESOURCES OP THE PHILIPPINES, I. 519 THE MILKFISHES. Family Chanid^. (PI. X) The five or milkfish Chanos chanos (Forskal), called baitgos, haiigod, kaivag-hawag, and iumulocso by the Filipinos and iangellus by the Moros, is one of the most important commercial fishes in the Islands."
        ),
    ]

    # model path can be set to a location at huggingface as shown below or local path to the training result serialized to out_path
    ner_pipeline = AutoPipeline.from_pretrained(
        "leonhardhennig/copious_ner", device=-1, num_workers=0
    )

    ner_pipeline(documents)

    for document in documents:
        for entity in sorted(document.entities.predictions, key=lambda x: x.start):
            print(f"{entity} -> {entity.label} ({entity.start}-{entity.end})")
        print("\n\n")


if __name__ == "__main__":
    predict()
