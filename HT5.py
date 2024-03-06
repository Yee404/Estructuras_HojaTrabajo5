import simpy
import random
import matplotlib as plt

Semilla = 0
Ram_Inicial = 100
Intervalo = 10
Velocidad = 3
Tiempos = []

random.seed(Semilla)

# Entorno de simulación
env = simpy.Environment()

# Simular memoria RAM
RAM = simpy.Container(env, init=Ram_Inicial, capacity=Ram_Inicial)

# Simular CPU/ procesador
CPU = simpy.Resource(env, capacity=1)

def Proceso(env, nombre, RAM, CPU):
    print(f"{nombre} llega al sistema en t = {env.now}")
    
    # Solicitar memoria RAM
    memoria_requerida = random.randint(1, 10)
    yield RAM.get(memoria_requerida)
    print(f"{nombre} obtiene {memoria_requerida} de memoria RAM en t = {env.now}")
    
    # Pasar a estado "Listo (ready)"
    with CPU.request() as req:
        yield req  # Esperar a que el CPU esté disponible
        print(f"{nombre} comienza a ejecutarse en el CPU en t = {env.now}")
        
        # Ejecutar instrucciones en el CPU
        instrucciones_restantes = random.randint(1, 10)
        while instrucciones_restantes > 0:  
            yield env.timeout(Velocidad)
            print(f"{nombre} ha ejecutado 3 instrucciones en t = {env.now}")
            
            # Actualizar el contador de instrucciones
            instrucciones_restantes -= 3
            if instrucciones_restantes <= 0:
                # El proceso ha terminado
                print(f"{nombre} ha terminado todas las instrucciones en t = {env.now}")

                # Lógica para determinar si Waiting, Ready o Terminated
                probabilidad_waiting = random.uniform(0, 1)
                if probabilidad_waiting <= 0.5:
                    # 50% de probabilidad de ir a Waiting
                    print(f"{nombre} va a la cola de Waiting")
                    yield env.timeout(1)  # Simula operaciones de I/O
                    print(f"{nombre} regresa a la cola de Ready desde Waiting")
                else:
                    # 50% de probabilidad de ir a Ready
                    print(f"{nombre} va a la cola de Ready")

                # Devolver la memoria RAM al finalizar
                yield RAM.put(memoria_requerida)
                print(f"{nombre} devuelve {memoria_requerida} de memoria RAM en t = {env.now}")
                print("\n")
                return

# Generador procesos
def llegada(env, RAM, CPU):
    # Ciclo infinito para simular llegada continua de procesos
    while True:
        proceso = env.process(Proceso(env, f"Proceso-{env.now}", RAM, CPU))
        Tiempo_llegada = env.now
        yield proceso
        Tiempos.append(env.now - Tiempo_llegada)

# Iniciar la simulación
env.process(llegada(env, RAM, CPU))
env.run(until=50)

# Calcular promedio y desviación estándar de tiempos de ejecución
promedio = sum(Tiempos) / len(Tiempos)
desviacion = (sum((t - promedio) ** 2 for t in Tiempos) / len(Tiempos)) ** 0.5

# Imprimir resultados
print("\n")
print(f"DATOS ESTADÍSTICOS DEL PROCESO:")
print(f"Promedio de tiempo de ejecución: {promedio}")
print(f"Desviación estándar: {desviacion}")
print("\n")
# Nota personal. Lo siguiente es info del error, problemas con las gráficas



## GRAFICAS
def Graficas(num_procesos):
    global Tiempos
    env = simpy.Environment()
    RAM = simpy.Container(env, init=Ram_Inicial, capacity=Ram_Inicial)
    CPU = simpy.Resource(env, capacity=1)

    Tiempos = []  # Reiniciar la lista de tiempos
    env.process(llegada(env, RAM, CPU, num_procesos))
    env.run(until=50)

    # Calcular promedio y desviación estándar de tiempos de ejecución
    promedio = sum(Tiempos) / len(Tiempos)
    desviacion = (sum((t - promedio) ** 2 for t in Tiempos) / len(Tiempos)) ** 0.5

    # Imprimir resultados
    print("\n")
    print(f"DATOS ESTADÍSTICOS DEL PROCESO ({num_procesos} procesos):")
    print(f"Promedio de tiempo de ejecución: {promedio}")
    print(f"Desviación estándar: {desviacion}")

    # Generar gráfica
    plt.plot(range(1, num_procesos + 1), Tiempos, marker='o')
    plt.title(f"Tiempo de ejecución para {num_procesos} procesos")
    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo de ejecución")
    plt.show()

# Llamar a la función con diferentes cantidades de procesos
Graficas(25)
Graficas(50)
Graficas(100)
Graficas(150)
Graficas(200)