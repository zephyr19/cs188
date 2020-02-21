# section3

1. **CSP: Air Traffic Control**

   1. formulation as CSP:

      1. variables: A, B, C, D, E
      2. domains: {i1, i2, i3, i4, d1, d2, d3, d4}
      3. constraints:
         1. time(B) = 1
         2. time(D) >= 3
         3. time(A) <= 2
         4. time(D) < time(C)
         5. value(i) != value(j) for i, j in variables

   2. ~~with addition constraints:~~

      1. ~~adding constraints:~~

         1. ~~runway(A) = runway(B) = runway(C) = i~~
         2. ~~runway(D) = runway(E) = d~~ 

      2. ~~constraint graph:~~

         1. ~~everybody connected each other~~

      3. |      |      | 0    | 0    |
         | ---- | ---- | ---- | ---- |
         |      | 0    | 0    | 0    |
         |      |      | 0    | 0    |
         | 0    | 0    |      | 0    |
         |      |      |      |      |

   3. O(nd^2^)

2. Games
   1.  4, 3, 2, 4
   2. 15, 7 will be pruned
   3. 8, 7, 8, 5
   4. Neither will be pruned, because u can't promise a expect node's value without checking it.
3. Nonzero-sum Games
   1. (15, 9), (3, 5), (15, 9), (4, 12)
   2. Neither will be pruned, because 

