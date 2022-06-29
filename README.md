# Protein-Po-w-der
## Intro
Voor deze case is het doel om zo stabiel mogelijke eiwitten te vouwen.
Eiwitten zijn complexe moleculen die cruciale rollen vervullen in het structureren en functioneren van het menselijk lichaam.
Ze zijn opgebouwd uit duizenden kleinere bouwstenen genaamd aminozuren die als een ketting aan elkaar vastzitten. 
De structuur van eiwitten wordt gevormd doordat ze op een bepaalde manier gevouwen worden.
Eiwitten worden vervolgens bij elkaar gehouden door verschillende chemische bindingen tussen aminozuren.
Deze case vraagt om een versimpeling van de werkelijkheid waarin de stabiliteit van een eiwit wordt weergegeven door een score.
Deze score wordt berekend door alle bindingen in een eiwit op te tellen 
Hierbij geldt hoe lager de score, hoe stabieler het eiwit. 
Een eiwit wordt gevouwen in een 2-dimensionale grid waarin vouwen naar links, rechts, onder en boven mogelijk is.
In realiteit zijn er twintig verschillende aminozuren, maar voor deze case zijn ze opgedeeld in groepen genaamd hydrofobe (H), polaire (P) en cysteïne (C) aminozuren.
Twee H's of één H en één C die naast elkaar liggen in de grid, maar niet direct verbonden zijn in de keten creëren een binding met score -1.
Twee C's in dezelfde situatie creëren een sterkere binding met score -5.
Door te spiegelen en te draaien, kunnen er mogelijkheden worden weggestreept bij de eerste twee vouwen.
Dit levert voor deze case de volgende state space formule op: 3^(n-2) * 2 (geldig vanaf n = 3) waarbij n het aantal vouwen is.

## Algoritmes

## Usage

