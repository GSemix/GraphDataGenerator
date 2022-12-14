Скрипт предназначен для генерации координат Вершин (Vertex.json) и Рёбер (Edges.json) графа по файлу SVG (сгенерированном в Adobe Illistrator).  
  
* Рёбра представлены списком смежности  
  
Правила:  
    Вершиной считается circle с [id] {  
        1. В начале [id] необходимо ставить '#' (этот символ не попадёт в [name] вершины)  
        2. Далее [name](не должен содержать '_')  
        3. Теперь через '_' добавляйте [name] вершин, которые связаны с текущей  
        
        [!] >> Для полностью валидного ввода [id] должен содержать любые буквы английского, русского алфавита и только разрешённые знаки (permittedHexSymbols.json), иначе программа предупредит об это (но если соблюдены 3 правила сверху, включит в граф)  
    }
      
Примеры:  
    Ввод SVG:  
        file.svg:  
            ...  
            <circle id="#[name]_[nameNeighboor1]_..._[nameNeighboorN]" .../>  
            ...  
      
        1. <circle id="#perehod&B&F&2_2074a_toilet&B&2&1_2008" class="st8" cx="211" cy="97" r="6.4"/>  
        2. <circle id="#2006b_2006a_2003a_2005b" class="st8" cx="583" cy="739.6" r="6.4"/>  
        3. <circle id="#2003_Переход&Г&1_2003а_2005б" class="st8" cx="583" cy="739.6" r="6.4"/>  
          
    Вывод JSON:  
        Vertex.json:  
            {  
                "[name]": {  
                    "housing": "[housing]",  
                    "floor": "[floor]",  
                    "x": "[cX]",  
                    "y": "[cY]"  
                },  
                    ...  
            }  
      
        Edges.json:  
            {  
                "[name]": [  
                    "[nameNeighboor1]",  
                        ...  
                    "[nameNeighboorN]"  
                ],  
                    ...  
            }  
              
Запуск:  
  
python3 generateOnText.py wayToFileSVG  
