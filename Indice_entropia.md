**Propuesta sobre un índice de esfuerzo utilizando entropía de Shannon**

De acuerdo con la base de datos referente a los tipos de trámites y servicios ofertados por las diferentes dependencias, se tienen variables de diferente categoría; el objetivo de utilizar esas variables es proponer un índice de esfuerzo asignado a cada trámite que permita cuantificar su nivel de complejidad.

Se distinguen las variables de la base que pueden aportar información cuantitativa de los trámites como su “Tiempo\_en\_minutos” que describe la duración en minutos aproximada de cada trámite; “N\_FORMATOS\_FINAL” es la cantidad de formatos que requiere el trámite; “CONTEO\_NETO” es la cantidad de requisitos; “nivel\_digitalizacion” indica el nivel de digitalización asignado a cada trámite correspondiente con 14 niveles determinados donde, entre más alto, más digitalización tiene; “TraCosto” es la confirmación sobre la existencia de algún costo en los trámites; y “Porcentaje\_Efectividad” indica el porcentaje de trámites cuyo proceso ha sido favorable.  
Debido a que “Porcentaje\_Efectividad” es un dato que se obtiene después de realizar el trámite, aporta información más sobre experiencia de usuario que sobre el proceso, entonces nos enfocaremos en cumplir el objetivo con las demás variables.

*.Hipótesis*

Dado que el objetivo es construir un índice de esfuerzo que indique el nivel de complejidad del trámite, se espera que cumpla las siguientes características:

* El índice de esfuerzo debe aumentar conforme aumenta la cantidad de formatos y requisitos.  
* El índice de esfuerzo debe aumentar conforme aumenta la cantidad de tiempo.  
* El índice de esfuerzo debe disminuir conforme aumenta el nivel de digitalización.  
* El índice de esfuerzo debe aumentar conforme lo hace  el costo del trámite.

*Teoría*  
*Entropía de Shannon*

Entropía de la información o de Shannon es una cantidad que mide la incertidumbre de una fuente de información de valores discretos, también interpretado como la cantidad de ruido o desorden que contiene.   
Como ejemplo, consideremos una distribución de datos cuyos valores caen dentro de una cierta cantidad de intervalos o son asignaciones discretas limitadas donde cada intervalo o asignación puede tener o la misma o distinta probabilidad de aparecer en la distribución por lo que los datos no son aleatorios. Observando la distribución, no podemos predecir cuál será el siguiente dato de la misma, lo que los haría de cierto modo aleatorios, sin embargo, la entropía de Shannon es la encargada de definir dicha aleatoriedad, cosa que fue presentada por Claude E. Shannon en un artículo de 1948\.

Shannon define que la entropía satisface las relaciones:

* Un pequeño cambio en la probabilidad de caer en cada intervalo o asignación debe traer consigo un pequeño cambio en la entropía.  
* Si todos los intervalos o asignaciones son equiprobables, la entropía es máxima.

Si para un evento X de “k” estados posibles cada uno tiene una probabilidad de aparecer $p\_i=p(x\_i)$, la entropía del evento X viene dada por la suma ponderada de la cantidad de información:  
$\\ H(X)=-\\sum\_i p(x\_i)logp(x\_i)\\$

*Autoinformación*

Es una cantidad que mide el nivel de sorpresa de un resultado particular de un evento X. Está relacionada con la entropía pues ésta es el valor esperado de la autoinformación de la variable midiendo así el nivel de sorpresa promedio de la variable.  
La autoinformación mide que, cuanto menos probable sea un resultado, más sorprendente será. Se define como:  
$\\ I(x\_i)=-log(p(x\_i))\\$  
Mientras que su relación con entropía es:  
$\\H(X)=\\sum\_i p(x\_i)I(x\_i)\\$

*Metodología*

Como se había mencionado, las variables tienen diferente categoría pero, en general se pueden discretizar, es por ello que se opta por generar el índice de esfuerzo utilizando entropía de Shannon.

El primer paso para ello es discretizar las variables. El nivel de digitalización es discreto habiendo solo 14 niveles; los números de formatos y requisitos también son discretos obteniendo un valor dependiendo del trámite; el costo es un valor binario, a fin de cuentas discreto, que determina si existe costo o no del trámite; finalmente, el tiempo, al ser una variable de valores muy grandes, su rango existe entre los 0 y los 518 mil minutos, prácticamente este dato permite cualquier valor en ese intervalo, por ello es posible considerarla como continua.

Debido a que los datos de tiempo caen dentro del rango de 0 a 518 mil minutos (1 año aproximadamente) podemos proponer el re-escalamiento de dicha variable en un rango más corto utilizando el logaritmo de los valores de tiempo. Como existen tiempos cero entonces sería necesario incluir el término "1+t" para el logaritmo.   
Podemos discretizar el tiempo asignando el rango de la transformación en este caso en 8 bins (grupos, intervalos) de igual tamaño en la escala logarítmica.    
Además, rellenamos valores nulos de tiempo con la mediana de tiempo de los trámites por dependencia para dependencias con muchos trámites y con el promedio de tiempo de los trámites por dependencia para dependencias con pocos trámites.   
Eliminamos también dos datos de tiempo que no tenían valor, considerando que el total de trámites era de 667, esos dos son insignificantes.

Para formatos y requisitos, a pesar de que son discretos, tienen pocas apariciones las cantidades altas, de modo que se opta por agrupar estas cantidades en 5 bins a cada variable para rescatar distribución.   
Definimos las funciones de entropía y su normalización teórica  
Las pruebas realizadas apuntan a que la entropía mejora con la agrupación y, de hecho, al casi no haber diferencia de entropía en formatos agrupados y no agrupados, podemos llegar a concluir en este punto que no todas las variables aportan de la misma forma a la cantidad de complejidad de los trámites.

Calculamos las entropías de todas las variables y observamos que el tiempo y costo dominan en cantidad. En este punto nos preguntamos cómo asignar complejidad a cada trámite si la entropía es general para las variables, es donde entra en juego la autoinformación, que asigna sorpresa a cada resultado posible de cada variable.

Para el tiempo, es posible distinguir dos tipos de complejidad, la primera es pura distribución (cosa que rescata entropía, autoinformación), qué tan variable es un dato respecto a los demás, y la segunda es sobre la duración de un trámite, que puede ser rescatado por una medida de nivel que describa la posición de cada dato, en este caso, optando por utilizar un z-score.  
Se calculó la autoinformación del tiempo así como el z-score para describir la complejidad del tiempo.  Se correlacionaron estas dos cantidades entre sí y se obtuvo una correlación cercana a 0, lo que indica que muestran cantidades independientes y representan enfoques distintos del tiempo.

Para generar la complejidad del tiempo se propone una combinación lineal de las características antes mencionadas de variabilidad (autoinformación) y duración (z.-score).   
$\\ indice\_{tiempo}=x\_1I(t)+x\_2Z\_{score}$\\  
Se realiza análisis PCA para esta parte pero como las variables son independientes el PCA las muestra ortogonales y solo las rota, arrojando que las dos componentes principales explican aproximadamente el 50% de los datos.  
Se opta por realizar análisis de sensibilidad sobre cambios en el índice al variar pesos de las componentes de la complejidad del tiempo respetando la siguiente relación.  
$\\ indice\_{tiempo}=wI(t)+(1-w)Z\_{score}\\$

Luego, se realizaron los rankings de las posiciones de los trámites utilizando un peso base y correlacionando con los rankings de un conjunto de pesos que van de 0 a 1 para formar un gráfico de estabilidad que muestra hasta qué valores de peso (w) es muy estable la correlación de rankings. Para este análisis se muestra que la elección de peso w=0.5 es de las más estables. Por lo tanto, el índice de complejidad del tiempo se toma como:  
$\\ indice\_{tiempo}=0.5I(t)+0.5Z\_{score}\\$

Construimos la autoinformación normalizada con el máximo para cada una de las otras variables y proponemos la construcción del índice de complejidad/esfuerzo como el promedio de estas autoinformaciones y el índice del tiempo. Además, se realiza otra propuesta de índice igual pero asignando pesos a cada variable, estos pesos surgen como el cociente entre la entropía de la variable correspondiente con la entropía total de cada trámite.  
Se correlacionaron estas dos propuestas y se encontró que su correlación es de 0.94, por lo que podemos utilizar cualquiera de estas, optando por la de pesos iguales, la primera propuesta de pesos 1\.

Una vez decidido el índice procedió a hacer la correlación de éste con cada una de las variables originales, mostrando que su correlación con el costo es negativa (entre más costo, menos complejo) lo que es contraintuitivo. La explicación es justo la distribución de los valores de costo, al ser 70% los que sí cuestan y 30% los que no, la variabilidad de lo datos es alta y le asigna mayor entropía a los datos, por lo que le da esta interpretación.  
Concluimos que no deberíamos poder usar entropía para la variable de costo por esta misma razón y que es mejor utilizar una forma directa de la variable. Optamos por usarla directamente.

Armamos de nuevo el índice de complejidad y correlacionamos de nuevo con las variables encontrando que el signo de correspondencia con el costo ya es correcto. Gracias a este análisis nos dimos cuenta que el nivel de digitalización tiene el mismo comportamiento, por lo que optamos por utilizarla reajustada para que muestre lo que queremos.

Volvemos a realizar el índice de complejidad con estas consideraciones y correlacionamos con las variables. Observamos que la correlación con el costo es la más alta y lo interpretamos porque justamente que tiene solo dos valores y tiene distribuciones distintas con gran variabilidad. Optamos por asignar pesos y realizamos PCA. El coeficiente mostrado para tiempo casi le quita toda su interpretación por lo que descartamos este método.

Como las variables describen escalas diferentes, optamos por aplicar z-score a cada una de ellas y volver a construir el índice.  
Una vez construido, aplicamos correlación con variables originales y se muestra más equilibrado, asignando mayores pesos a requisitos y formatos, le baja el peso a costo, el tiempo tiene peso bajo y la digitalización es inversa.

*Análisis de resultados*

Una vez decidida la estructura del índice, se procedió a hacer gráficos representativos sobre sus características. Uno de los más informativos es el gráfico de complejidad vs duración de trámite, en este gráfico prácticamente se muestra que no hay dominancia del tiempo en el índice pues hay trámites cortos que son muy complejos tanto como hay trámites muy largos que son medianamente complejos.

Otro gráfico es el de comparación promedio de los valores dimensionales componentes del índice para el top 10 más complejos y el top 10 menos complejos. En este gráfico destaca que los más complejos tienen altos niveles en requisitos y formatos mientras que los menos complejos son bajos, este es el factor principal de complejidad. La digitalización es el segundo gran factor pues para los menos complejos se ven valores muy bajos. El tiempo y el costo son factores moderados.

Luego de esto, se realizó un análisis con K.means para distinguir subgrupos de las componentes dimensionales del índice que permitan describir las características de los trámites. Usando el método del codo, se determinaron 4 clusters para apicar en K-means.  
Luego de usar K-means para 4 clusters se distingue que el cluster 0 es aquel para trámites altamente digitalizados y lentos; el cluster 1 tiene trámites estándar que cuestan, siendo un enfoque más económico; el cluster 2 es para trámites simples y gratuitos, indicando trámites eficientes; finalmente, el cluster 3 es para trámites con muchos formatos y requisitos, básicamente indicando alta burocracia.

Agrupar las dependencias por porcentaje de trámites que estén dentro de cada cluster nos puede ayudar a distinguir los puntos débiles de las mismas o sus puntos fuertes.

*Conclusiones*

Como conclusión general, se permitió construir un índice de esfuerzo/complejidad administrativa considerando requisitos, formatos, nivel de digitalización, costo y tiempo de cada trámite como una combinación de estas dimensiones.  
Se mostró con base en este índice que la complejidad no está dominada por el tiempo, incluso, hay trámites muy largos no tan complejos y hay trámites cortos muy complejos. Incluso, los más complejos eran mayormente burocráticos.

En general, los trámites más complejos tenían altos requisitos, altos formatos y baja digitalización mientras que costo y tiempo eran moderadamente considerados.

La modificación de la digitalización permitió identificar qué trámites más simples son más digitalizados y que los más complejos son menos digitalizados.

La construcción de un índice híbrido específicamente para el tiempo fue una elección correcta. Identificar que existen dos tipos de complejidad temporal basada en duración y en rareza o información permitió juntar estas dos características y no solo basar el índice correspondiente en un solo parámetro. Además, los análisis de sensibilidad mostraron estabilidad en la elección de los pesos.

Es destacable mencionar que el índice construido es relativo al sistema y no absoluto.  
El uso de K-means permitió distinguir diferentes tipos de complejidad de cada trámite, indicando alta burocracia, alta digitalización, presencia de costos y eficiencia. Por ello, la complejidad de trámites no es homogénea y la mejora en trámites debería incluir políticas públicas distintas.

El modelo identifica outliers que no representan el promedio del sistema pero muestran áreas de intervención.  
El modelo mostró estabilidad al comparar rankings entre ponderaciones, por lo que no depende excesivamente de una ponderación arbitraria.

El uso de entropía permitió identificar rareza administrativa, complejidad estructural y distinguir trámites poco comunes.  
En algunos casos, como en el costo, el uso de autoinformación hacía ver a aquellos trámites gratuitos como más complejos, sin embargo hay diferencia de interpretación, en este caso el costo no debería tratarse como rareza, sino como una barrera económica, por ello se incorporó directamente en el índice.

Finalmente, la complejidad administrativa no es principalmente temporal, sino estructural y documental.