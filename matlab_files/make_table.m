function [patients] = make_table()
    LastName = ["Sanchez";"Johnson";"Zhang";"Diaz";"Brown"];
    Age = [38;43;38;40;49];
    Smoker = [true;false;true;false;true];
    Height = [71;69;64;67;64];
    Weight = [176;163;131;133;119];
    BloodPressure = [124 93; 109 77; 125 83; 117 75; 122 80];

    patients = table(LastName,Age,Smoker,Height,Weight,BloodPressure)