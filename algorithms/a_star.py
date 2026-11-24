import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (admissível)."""
        distance = 0
        for idx, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            curr_row, curr_col = divmod(idx, 3)
            goal_row, goal_col = divmod(tile - 1, 3)
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        start_h = self.heuristic(initial)
        frontier = [(start_h, 0, initial)]  # (f_score, counter, estado)
        counter = 0
        visited = {initial: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            f, _, current = heapq.heappop(frontier)
            nodes_expanded += 1
            max_frontier_size = max(max_frontier_size, len(frontier))

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            for child in current.neighbors():
                nodes_generated += 1
                g = child.cost
                if child not in visited or g < visited[child]:
                    visited[child] = g
                    h = self.heuristic(child)
                    counter += 1
                    heapq.heappush(frontier, (g + h, counter, child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=-1,
        )