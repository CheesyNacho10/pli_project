(define (problem bloques)
  (:domain bloques)
  (:objects a b c - bloque)
  (:init
    (clear a) (clear b) (clear c)
    (ontable a) (ontable b) (ontable c)
    (handempty)
  )
  (:goal (and (on a b) (on b c)))
)