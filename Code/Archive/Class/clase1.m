% limpiar pantalla
clc;
% limpiar variables
%clear all; % No tan recomendando porque clear ya lo realiza
% cerrar figuras
close all;
% Desactivar alertas
warning off all; 
% Disp: Muestra un mensaje en la consola
disp('Fin del programa');

% Calcular centroide de una matriz sin usar mean
C1 = [0,1,2,4; 0,2,3,5];
C2 = [5,7,6,8; 6,4,9,4];

% mostrar clases
plot(C1(1,:), C1(2,:), 'ro'); % Clase 1 en rojo
% grid on: Agrega una cuadrícula al gráfico
grid on;
hold on; % Mantener el gráfico para agregar más elementos
plot(C2(1,:), C2(2,:), 'bo'); % Clase 2 en azul
hold on; % Mantener el gráfico para agregar más elementos
legend('Clase 1', 'Clase 2'); % Agregar leyenda al gráfico

coordenadaX= input("Ingrese la coordenada X del punto a clasificar: ");
coordenadaY= input("Ingrese la coordenada Y del punto a clasificar: ");
X = [coordenadaX; coordenadaY];
plot (X(1), X(2), 'r>'); % Punto a clasificar
hold on; % Mantener el gráfico para agregar más elementos
legend('Clase 1', 'Clase 2', 'Punto a clasificar'); % Actualizar leyenda

% Calcular centroides de cada clase
sumaX_CL1 = sum(C1(1,:));
sumaY_CL1 = sum(C1(2,:));
sumaX_CL2 = sum(C2(1,:));
sumaY_CL2 = sum(C2(2,:));

centroide_CL1 = [sumaX_CL1/length(C1(1,:)); sumaY_CL1/length(C1(2,:))];
centroide_CL2 = [sumaX_CL2/length(C2(1,:)); sumaY_CL2/length(C2(2,:))];

% Mostrar centroides
plot(centroide_CL1(1), centroide_CL1(2), 'gs'); % Centroide de clase 1 en verde
hold on; % Mantener el gráfico para agregar más elementos
plot(centroide_CL2(1), centroide_CL2(2), 'gs'); % Centroide de clase 2 en verde
legend('Clase 1', 'Clase 2', 'Punto a clasificar', 'Centroides'); % Actualizar leyenda

% Calcular distancia euclidiana entre el punto a clasificar y los centroides
distancia_CL1 = sqrt((X(1) - centroide_CL1(1))^2 + (X(2) - centroide_CL1(2))^2);
fprintf('Distancia al centroide de Clase 1: %.2f\n', distancia_CL1);
distancia_CL2 = sqrt((X(1) - centroide_CL2(1))^2 + (X(2) - centroide_CL2(2))^2);
fprintf('Distancia al centroide de Clase 2: %.2f\n', distancia_CL2);

minimo = min(distancia_CL1, distancia_CL2);
fprintf('La distancia mínima es: %.2f\n', minimo);
index = find([distancia_CL1, distancia_CL2] == minimo);
fprintf('El punto pertenece a la Clase %d\n', index);

% Clasificar el punto según la distancia más corta
if distancia_CL1 < distancia_CL2
    disp('El punto pertenece a la Clase 1');
else
    disp('El punto pertenece a la Clase 2');
end
