(* Implementation of the quicksort algorithm *)

let rec qsort = function
   | [] -> []
   | pivot :: rest ->
     let is_less x = x < pivot in
     let left, right = List.partition is_less rest in
     qsort left @ [pivot] @ qsort right