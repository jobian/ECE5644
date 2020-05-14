# ECE5644 (Prof. Walid Saad), Demetrius Davis - Spring 2020
Final Game Theory course project

# Default (modifiable) settings:
- Number of runs: 100 (each 'run' is a series of repeated games, ran until system failure)
- Number of nodes: 100
- Defense budget: 50 (half of node count)
- Goal node index: 94
- Default radio transmission range: 18
- Byzantine failure threshold, 50% of nodes inactive (compromised and/or quarantined)
- Bad guy location: 25, 25
- Player utilities (Normal form):
* Defender/Covered = 3, Defender/Uncovered = -1
* Attacker/Covered = -2, Attacker/Uncovered = 1
- Iteratively draw the network graph (DRAW_GRAPH=True)
    *Recommend also setting the flag ONE_SEC_DELAY=True to allow the chart to update
