# Protein-Po-w-der
## Intro
Voor deze case is het doel om zo stabiel mogelijke eiwitten te vouwen.
Eiwitten zijn complexe moleculen die cruciale rollen vervullen in het structureren en functioneren van het menselijk lichaam.
Ze zijn opgebouwd uit duizenden kleinere bouwstenen genaamd aminozuren die als een ketting aan elkaar vastzitten. 
De structuur van eiwitten wordt gevormd doordat ze op een bepaalde manier gevouwen worden.
Eiwitten worden vervolgens bij elkaar gehouden door verschillende chemische bindingen tussen aminozuren.
Deze case vraagt om een versimpeling van de werkelijkheid waarin de stabiliteit van een eiwit wordt weergegeven door een score.
Deze score wordt berekend door alle bindingen in een eiwit op te tellen.
Hierbij geldt hoe lager de score, hoe stabieler het eiwit. 
Een eiwit wordt gevouwen in een 2-dimensionale grid waarin vouwen naar links, rechts, onder en boven mogelijk zijn.
In realiteit zijn er twintig verschillende aminozuren, maar voor deze case zijn ze opgedeeld in groepen genaamd hydrofobe (H), polaire (P) en cysteïne (C) aminozuren.
Twee H's of één H en één C die naast elkaar liggen in de grid, maar niet direct verbonden zijn in de keten creëren een binding met score -1.
Twee C's in dezelfde situatie creëren een sterkere binding met score -5.
Door te spiegelen en te draaien, kunnen er mogelijkheden worden weggestreept bij de eerste twee vouwen.
Dit levert voor deze case de volgende state space formule op: 3^(n-2) * 2 (geldig vanaf n = 3) waarbij n het aantal vouwen is.

## Algoritmes

### Random algoritme
Dit algoritme gaat alle aminozuren in volgorde af en vouwt deze in willekeurige richtingen. Het algoritme bepaalt dus per aminozuur wat de mogelijke vouwrichtingen zijn en kiest hiervan een rondom richting. Het algoritme stopt zodra alle aminozuren, behalve de laatste, gevouwen zijn.

### Depth-first algoritme
Het Depth-first algoritme is een constructief algoritme dat de garantie voor de optimale oplossing kan leveren. Het algoritme bekijkt voor elk amino alle mogelijke richtingen en maakt daarvoor een apart eiwit aan. Elk aangemaakte eiwit wordt op een LIFO-stack gegooit. Daarna neemt het algoritme het laatste eiwit van de stack en herhaalt hij het recept totdat elke amino een richting heeft. Als dit complete eiwit een betere stabiliteit heeft dan ons huidige eiwit dan slaan we dit op als ons huidige eiwit. Zo gaat het algoritme de hele state space af, waardoor het dus de optimale oplossing kan leveren. 

### Hill climbing algoritme
Bij het hillclimbing algoritme wordt gestart met een random gevouwen eiwit. Dit eiwit wordt als startpunt gebruikt. Het algoritme bevat een functie die ervoor zorgt dat het eiwit op een willekeurige plek een willekeurige kant opgevouwen wordt. Wanneer dit een geldig eiwit oplevert met een hogere stabiliteit dan wordt deze opgeslagen en dan wordt de vorige stap herhaald. Als het algoritme n keer geen verbetringen meer oplevert dan wordt de best gevonden oplossing terug gestuurd en wordt het proces herhaald vanaf een nieuw willekeurig startpunt. Dit gaat door tot het opgegeven aantal runs. 

### Parallel Hill climbing algoritme
Het parellele hilclimbing algoritme werkt hetzelfde als het hillclimber algoritme, maar in plaats van dat het aantal runs in volgorde wordt uitgevoerd, gebeurt dat nu via multi processing parallel. Dit zorgt ervoor dat het significant sneller is en hetzelfde resultaat oplevert. 

### Simulated annealing algoritme
Het simulated annealing algoritme lijkt erg op het hillclimber algoritme, behalve dat geldige eiwitten met een slechtere stabiliteit soms wel worden opgeslagen. Het wel of niet opslaan van eiwitten met een slechtere stabiliteit is afhankelijk van de temperatuur die langzamerhand kouder wordt en in hoeverre het eiwit een verslechterde stabiliteitsscore heeft ten opzichte van het als laatst opgeslagen eiwit. De temperatuur is afhankelijk van hoelang het algoritme draait. Hoe langer het algoritme draait hoe kouder de temperatuur.


## Usage

