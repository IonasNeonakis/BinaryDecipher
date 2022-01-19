package fr.univ.test_apk_analyse_1_ok;

import fr.univ.test_apk_analyse_1_ok.inheritance.Animal;
import fr.univ.test_apk_analyse_1_ok.inheritance.Canide;
import fr.univ.test_apk_analyse_1_ok.inheritance.Chien;

public class CheckCast {

    public void check(){
        Chien chien = new Chien();
        Animal chien_abstract = new Chien();

        if(chien instanceof Animal){
            System.out.println("Chien est bien instanceof Animal");
        }

        if(chien_abstract instanceof Canide){
            System.out.println("instanceof Canide");
        }
    }
}
