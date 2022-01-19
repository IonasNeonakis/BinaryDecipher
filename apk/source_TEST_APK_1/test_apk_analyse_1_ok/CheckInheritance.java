package fr.univ.test_apk_analyse_1_ok;

import fr.univ.test_apk_analyse_1_ok.inheritance.Animal;
import fr.univ.test_apk_analyse_1_ok.inheritance.Chien;

public class CheckInheritance {
    public static void check(){
        Animal a = null;
        Chien samir = null;
        samir = new Chien();
        a.genericSound();
        samir.genericSound();
        samir.canideSound();
        samir.bark();
    }
}
