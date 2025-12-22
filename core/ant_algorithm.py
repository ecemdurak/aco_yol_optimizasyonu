# core/ant_algorithm.py
import numpy as np
import random


class AntColonyOptimization:
    def __init__(self, distances, n_ants, n_iterations, alpha, beta, evaporation_rate):
        self.distances = distances  # Mesafe matrisi
        self.n_cities = len(distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha  # Feromon önemi
        self.beta = beta  # Mesafe önemi (heuristic)
        self.rho = evaporation_rate  # Buharlaşma oranı

        # Feromon matrisini başlat (Başlangıçta küçük bir değer, 0 olmasın)
        self.pheromones = np.ones((self.n_cities, self.n_cities)) * 0.1

        # En iyi çözüm hafızası
        self.global_best_route = None
        self.global_best_distance = float('inf')

        # İterasyon geçmişi (Grafik için)
        self.history_best_distances = []

    def run(self):
        """Algoritmayı çalıştırır"""
        for iteration in range(self.n_iterations):
            all_routes = []
            all_distances = []

            # Her karınca için tur oluştur
            for ant in range(self.n_ants):
                route, dist = self._construct_solution()
                all_routes.append(route)
                all_distances.append(dist)

                # Global en iyi güncelleniyor mu?
                if dist < self.global_best_distance:
                    self.global_best_distance = dist
                    self.global_best_route = route

            # Feromonları güncelle
            self._update_pheromones(all_routes, all_distances)

            # Bu iterasyonun en iyisini kaydet
            self.history_best_distances.append(self.global_best_distance)

        return self.global_best_route, self.global_best_distance, self.history_best_distances

    def _construct_solution(self):
        """Bir karınca için tam bir tur oluşturur"""
        start_node = 0  # Isparta Merkez (veya rastgele)
        route = [start_node]
        visited = set([start_node])
        current = start_node
        total_dist = 0

        for _ in range(self.n_cities - 1):
            next_node = self._select_next_node(current, visited)
            route.append(next_node)
            visited.add(next_node)
            total_dist += self.distances[current][next_node]
            current = next_node

        # Başlangıça dönüş
        total_dist += self.distances[current][start_node]
        route.append(start_node)

        return route, total_dist

    def _select_next_node(self, current, visited):
        """Rulet tekerleği mantığı ile bir sonraki şehri seçer"""
        probabilities = []
        possible_nodes = []

        for node in range(self.n_cities):
            if node not in visited:
                possible_nodes.append(node)

                # Formül: (tau^alpha) * (eta^beta)
                tau = self.pheromones[current][node]
                # Eta (Çekicilik) = 1 / mesafe
                dist = self.distances[current][node]
                eta = 1.0 / dist if dist > 0 else 1.0

                prob = (tau ** self.alpha) * (eta ** self.beta)
                probabilities.append(prob)

        # Olasılıkları normalize et
        prob_sum = sum(probabilities)
        if prob_sum == 0:
            # Eğer tüm olasılıklar 0 ise rastgele seç (hata önleyici)
            return random.choice(possible_nodes)

        normalized_probs = [p / prob_sum for p in probabilities]

        # Rulet seçimi (numpy choice ağırlıklı seçim yapar)
        next_node = np.random.choice(possible_nodes, p=normalized_probs)
        return next_node

    def _update_pheromones(self, routes, distances):
        """Buharlaşma ve Yeni Feromon Ekleme"""
        # 1. Buharlaşma
        self.pheromones *= (1 - self.rho)

        # 2. Yeni Feromon Ekleme
        for route, dist in zip(routes, distances):
            contribution = 1.0 / dist  # Yol ne kadar kısaysa katkı o kadar büyük
            for i in range(len(route) - 1):
                u, v = route[i], route[i + 1]
                # Simetrik matris olduğu için iki yöne de ekleyebiliriz
                self.pheromones[u][v] += contribution
                self.pheromones[v][u] += contribution