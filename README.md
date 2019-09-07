# Comparer

Comparer jest aplikacją pozwalającą na porównanie działania algorytmów detekcji obiektów bazując na parametrach mAP (dokładność), precyzji, pokrycia oraz czasu jego działania. Możliwe jest również określenie pokrycia dla każdej z wykrytych klas obiektów z osobna. 


## Dane wejściowe

Aktualnie aplikacja jest skonfigurowana do porównania trzech algorytmów - SSD, Faster RCNN oraz YOLO. Aby aplikacja działała poprawne pliki wynikowe algorytmów powinny znaleźć się w odpowiednim folderze dla każdego z nich w głównym katalogu aplikacji. Poprawna struktura katalogów wygląda następująco:
```
├── nazwa_algorytmu
    ├── project_name
        ├── video_name
            ├── boxes
            │   ├── box1.json
            │   ├── box1.json
            │   ├── ...
            ├── frames
            │   ├── frame1.jpg
            │   ├── frame2.jpg
            │   ├── ...
            ├── time
                ├── time.json
```
     
Katalog boxes zawiera pliki opisujące położenie i klasę wykrytych obiektów. Powinny mieć one następującą strukturę:

```
[
  {
    "label": "person",
    "confidence": 0.15,
    "topleft": {
      "x": 0,
      "y": 327
    },
    "bottomright": {
      "x": 135,
      "y": 617
    }
  },
  {
    "label": "bird",
    "confidence": 0.4,
    "topleft": {
      "x": 723,
      "y": 327
    },
    "bottomright": {
      "x": 970,
      "y": 634
    }
  }
]
```
Katalog frames zawiera kolejne klatki badanego filmu. W folderze time znajdziemy plik z czasem pracy badanego algorytmu.

## Dane wyjściowe

Dane wyjściowe są zapisywane w katalogu 'out'. Składają się z plików json opisujących kolejne klatki np.

```
{
  "statistics": [
    {
      "alghorithmName": "ssd",
      "class_recall": [
        {
          "class_name": "bicycle",
          "recall": 0.75
        },
        {
          "class_name": "person",
          "recall": 0.75
        }
      ],
      "mAp": 0.5854439682991398,
      "precision": 0.5454545454545454,
      "recall": 0.75,
      "time": 103.02182197570801
    }
  ],
  "frame": [
    {
      "groundTruthBox": {
        "topleft_x": 240,
        "topleft_y": 199,
        "downright_x": 490,
        "downright_y": 365,
        "object_class": "bicycle"
      },
      "predictedBox": {
        "topleft_x": 219,
        "topleft_y": 194,
        "downright_x": 482,
        "downright_y": 362,
        "object_class": "bicycle"
      },
      "iou": 0.8537092178830787
    }
```
oraz z pliku w podfolderze 'statistics', który zawiera informacje o całym filmie. Przykład pliku statistics:

```
{
  "finalStatistics": [
    {
      "alghorithmName": "ssd",
      "mAP": 0.6145309568203107,
      "recall": 0.8896112141826419,
      "precision": 0.6834619400207629,
      "time": 103.02182197570801,
      "class_recall": [
        {
          "class_name": "bicycle",
          "recall": 0.9077142857142861
        },
        {
          "class_name": "person",
          "recall": 0.8761904761904765
        }
      ]
    }
  ]
}
```

Aplikacja składa się ze swojej bazowej funcjonalności, czyli analizy wyników algorytmów detekcji obiektów, ale również zawiera skrypty pomocnicze, pomagające edytować obraz, rysować bounding boxy na poszególnych klatkach, czy też konwertować wynikowy plik z formatu json na plik excel. 

## Uruchomienie aplikacji

Aplikacja jest uruchamiana poprzez poniższy skrypt. Musimy podać nazwę projektu, nazwę wideo oraz listę klas obiektów, które znajdują się na twoim filmie.

```
python3 comparer.py project_name video_name --available_classes available_classes list
```
np.
```
python3 comparer.py animals_project animals --available_classes available_classes cat dog sheep cow
```

## Tworzenie ground truth box oraz zmodyfikowanych filmów


```
python3 frames_creator.py project_name video_name format
```

Aby stworzyć niezmieniony zbiór klatek na podstawie filmu nazwa projektu oraz wideo musi być taka sama. Jeżeli chcemy utworzyć zmodyfikowany obraz musimy dodać odpowiedni przedrostek
```
przyciemniony obraz: video_name = dark_project_name
rozjaśniony obraz: video_name = dark_project_name
rozmazany obraz: video_name = blur_project_name
```
np.

```
python3 frames_creator.py cats dark_cats avi
```
