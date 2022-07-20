(define (problem tempsense) (:domain covisstorage)

(:objects 
  occ_val temp_val ac_val heat_val light_val blind_val w_val c_val l_val)

(:init
    (Is_Un_Occupied occ_val)
    (Is_Temp_High temp_val)
    (Is_CO2_normal c_val )
    (Is_Light_Normal l_val )
)

(:goal (and(or 
    (Heating_Off heat_val)
    (Heating_High heat_val)
    (Heating_Medium heat_val))
    (or
    (AC_On ac_val)
    (AC_Off ac_val))
    (or
    (Window_Closed w_val)
    (Window_Open w_val)
    (Window_Mid_Open w_val)
    )
    (or
    (Blind_Closed blind_val)
    (Blind_Open blind_val))
    (or
    (Lights_On l_val)
    (Lights_Off l_val))
)

)
)
