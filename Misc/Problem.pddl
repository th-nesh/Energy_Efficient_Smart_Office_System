(define (problem smartProblem) 
    (:domain Smart_Office_domain)
    (:objects 
    ac_on, ac_off, win_o, win_m, win_c, blind_o, blind_c, heat_h, heat_m, heat_off, light_on, light_off, un_oc, tl,o,lg,cn
    )

    (:init
        ;todo: put the initial state's facts and numeric values here
        (Is_Occupied uo)
        (Is_Temp_Low tl) 
        (Is_Light_Gloomy lg) 
        (Is_CO2_normal cn) 
    )

    (:goal(and  (or(AC_On ac_on)(AC_Off ac_off)) 
               (or (Window_Open win_o)(Window_Mid_Open win_m)(Window_Closed win_c))
               (or (Heating_High heat_h) (Heating_Medium heat_m) (Heating_Off heat_off))
               (or (Blind_Open blind_o) (Blind_Closed blind_c))
               (or (Lights_On light_on)(Lights_Off light_off)))

        
    )
)

;un-comment the following line if metric is needed
;(:metric minimize (???))


