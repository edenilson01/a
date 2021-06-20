/*
Programacion Logica con Prolog

- Autor: Edenilson Osnar Dominguez Amarilla
- Paradigmas de la Programacion*/

% HECHOS

% es_persona(x,y) x representa el nombre, y representa el apellido de la persona
es_persona(eliana, dominguez).
es_persona(edenilson, dominguez).
es_persona(elisa, amarilla).
es_persona(manuel, dominguez).
es_persona(isabel, jerez).
es_persona(lizz, bareiro).
es_persona(catalina, alvarenga).
es_persona(mario, villalba).
es_persona(richard, cabrera).

% representa que la persona tiene un ruc asociando
ruc_persona(es_persona(eliana, dominguez), 6799133).
ruc_persona(es_persona(edenilson, dominguez), 5012729).
ruc_persona(es_persona(elisa, amarilla), 1583885).
ruc_persona(es_persona(manuel, dominguez), 729042).
ruc_persona(es_persona(isabel, jerez), 4246441).
ruc_persona(es_persona(lizz, bareiro), 5127864).
ruc_persona(es_persona(catalina, alvarenga), 7000432).
ruc_persona(es_persona(mario, villalba), 2457801).
ruc_persona(es_persona(richard, cabrera), 4723651).

% representa los atributos de un articulo
articulo(1, shampoo, 1500, und).
articulo(2, 'purina para perro', 6000, kg).
articulo(3, mayonesa, 3000, und).
articulo(4, prestobarba, 5000, und).
articulo(5, galletita, 3000, und).
articulo(6, aceite, 7000, und).
articulo(7, 'queso rallado', 3500, und).

% representa las boletas de ventas generadas por la despensa
boleta(1, ruc_persona(es_persona(eliana, dominguez), 6799133), [articulo(1, shampoo, 1500, und), articulo(5, galletita, 3000, und)]).
boleta(2, ruc_persona(es_persona(catalina, alvarenga), 7000432), [articulo(4, prestobarba, 5000, und)]).
boleta(3, ruc_persona(es_persona(richard, cabrera), 4723651), [articulo(6, aceite, 7000, und), articulo(7, 'queso rallado', 3500, und), articulo(3, mayonesa, 3000, und)]).
boleta(4, ruc_persona(es_persona(eliana, dominguez), 6799133), [articulo(1, shampoo, 1500, und), articulo(5, galletita, 3000, und)]).

% REGLAS

% para saber si un determinado Nombre, Apellido y Ruc estan registrados como clientes
es_cliente(Nombre, Apellido, Ruc) :- ruc_persona(es_persona(Nombre, Apellido), Ruc).
% para saber si se cuenta con un articulo registrado con ese Codigo
es_articulo(Codigo) :- articulo(Codigo, _, _, _).
% para saber si se cuenta con una boleta registrada con el Codigo
existe_boleta(Codigo) :- boleta(Codigo, _, _).
% para saber si se cuenta registrado una boleta con el Ruc de un cliente especifico
realizo_compra(Ruc) :- boleta(_, ruc_persona(_,Ruc),_).
/*para saber cuantas veces un cliente realizo una compra, es decir cuantas boletas se tienen
	registradas de un determinado cliente a traves de su Ruc
  Si recibe dos variables logicas, devuelve la cantidad total de boletas generadas
  Si recibe el Ruc pero Cant como variable logica, devuelve la cantidad de boletas en las que
  	figura el cliente*/
cantidad_compras_cliente(Ruc, Cant) :- findall(Cliente, boleta(_,ruc_persona(Cliente, Ruc),_), Clientes), length(Clientes, Cant).