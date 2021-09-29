# -*- coding: utf-8 -*-

from xml.dom import minidom
import os
import glob

lut={}
lut["17cha_pet"]                            =0
lut["2% peach_pet"]                         =1
lut["2%_can"]                               =2
lut["aloe_pet"]                             =3
lut["ambasa_can345"]                        =4
lut["bacchus F_pet"]                        =5
lut["baeksansu_pet"]                        =6
lut["black_pet"]                            =7
lut["blackbori_light_pet"]                  =8
lut["bongbong_can"]                         =9
lut["burdock_tea_pet"]                      =10
lut["cantata americano_can"]                =11
lut["cantata latte_can"]                    =12
lut["cantata_americano_can200"]             =13
lut["cantata_americano_pet"]                =14
lut["cantata_latte_can390"]                 =15
lut["cantata_peanut_can"]                   =16
lut["cassiatora tea_pet"]                   =17
lut["ceylon tea_can"]                       =18
lut["cheonyeon_can355"]                     =19
lut["cider_can"]                            =20
lut["cider_lowersugar_can"]                 =21
lut["cider_pet"]                            =22
lut["coca_can"]                             =23
lut["coca_pet"]                             =24
lut["cocopalm_can"]                         =25
lut["colombiana_master_black_pet500"]       =26
lut["colombiana_master_latte_pet500"]       =27
lut["condition_lady_pet"]                   =28
lut["condition_pet"]                        =29
lut["conditionCEO_pet"]                     =30
lut["confidence_pet"]                       =31
lut["contrabass latte_pet"]                 =32
lut["contrabass_pet"]                       =33
lut["daily C_pet"]                          =34
lut["dawn1004_can"]                         =35
lut["dawn808_can"]                          =36
lut["demisoda_can"]                         =37
lut["demisoda_orange"]                      =38
lut["dr.pepper_can"]                        =39
lut["e-L_pet"]                              =40
lut["empty"]                                =41
lut["fanta orange_pet"]                     =42
lut["fanta pine_pet"]                       =43
lut["flower_tea_pet"]                       =44
lut["fruitcider_kiwi_pet"]                  =45
lut["fruitcider_pine_pet"]                  =46
lut["G_original_pet"]                       =47
lut["G_sparkling_pet"]                      =48
lut["galbae_can"]                           =49
lut["galbae_pet"]                           =50
lut["gatorade_pet"]                         =51
lut["georgia_craft_latte_pet470"]           =52
lut["georgia_latte_can240"]                 =53
lut["georgia_max_can"]                      =54
lut["georgia_original_can"]                 =55
lut["getorade_can"]                         =56
lut["gotica_americano_can"]                 =57
lut["gotica_latte_can"]                     =58
lut["gotica_vintage_black_can390"]          =59
lut["gotica_vintage_latte_can390"]          =60
lut["grape100_pet"]                         =61
lut["green plum_pet"]                       =62
lut["green_smoothie_pet"]                   =63
lut["greentea_pet"]                         =64
lut["hongsam_pet"]                          =65
lut["hot6_can"]                             =66
lut["hot6_thekingpower_can"]                =67
lut["hutgaecha_pet"]                        =68
lut["hutgaesoo_EX_pet"]                     =69
lut["hutgaesoo_pet"]                        =70
lut["hwal_pet"]                             =71
lut["icis8.0_pet"]                          =72
lut["ion the fit_pet"]                      =73
lut["jeju_pet"]                             =74
lut["jinssanghwa_pet"]                      =75
lut["kkaesugang_can"]                       =76
lut["leblen_grapefruit_pet"]                =77
lut["leblen_peach_pet"]                     =78
lut["lemona_pet"]                           =79
lut["lemona_sparkling_can"]                 =80
lut["lemonade_pet"]                         =81
lut["let's be mild_can"]                    =82
lut["let's be salt_can"]                    =83
lut["let's be trip_can"]                    =84
lut["let'sbe_cafetime_americano_can"]       =85
lut["let'sbe_cafetime_latte_can"]           =86
lut["let'sbe_grande_latte_pet500"]          =87
lut["lipton_can"]                           =88
lut["lipton_pet"]                           =89
lut["Lu-10_pet"]                            =90
lut["mango_can"]                            =91
lut["matcha_pet"]                           =92
lut["mate tea_pet"]                         =93
lut["mccol_can"]                            =94
lut["mccol_pet"]                            =95
lut["miero_fiber"]                          =96
lut["milkis_can"]                           =97
lut["milkis_pet"]                           =98
lut["minutemaid_apple_can"]                 =99
lut["minutemaid_grape_can"]                 =100
lut["minutemaid_peach_can"]                 =101
lut["mogumogu_peach"]                       =102
lut["mogumogu_pet"]                         =103
lut["monster_can"]                          =104
lut["morning_pet"]                          =105
lut["morningcare_D"]                        =106
lut["morningcare_H"]                        =107
lut["mtdew_can"]                            =108
lut["omija_pet"]                            =109
lut["oranC_can"]                            =110
lut["oronaminC_pet"]                        =111
lut["ourtea_lemon_pet"]                     =112
lut["ourtea_orange_pet"]                    =113
lut["peach_can"]                            =114
lut["pepsi_can"]                            =115
lut["pepsi_pet"]                            =116
lut["pocari_can"]                           =117
lut["pocari_pet"]                           =118
lut["power_can"]                            =119
lut["redbull_can"]                          =120
lut["rice_pet"]                             =121
lut["samdasoo_pet"]                         =122
lut["seagram_lemon_pet"]                    =123
lut["sky_pet"]                              =124
lut["smoothieking_original_pet"]            =125
lut["smoothieking_pine_pet"]                =126
lut["softwater_peach_pet"]                  =127
lut["sol_can"]                              =128
lut["sprite_can"]                           =129
lut["sprite_pet"]                           =130
lut["ssaekssaek_can"]                       =131
lut["starbucks_can"]                        =132
lut["starbucks_cream_can"]                  =133
lut["starbucks_pike_can"]                   =134
lut["tejava_can"]                           =135
lut["tomato_pet"]                           =136
lut["top americano_can"]                    =137
lut["top latte_can"]                        =138
lut["top_americano_can200"]                 =139
lut["top_americano_pet"]                    =140
lut["top_americano_pet380"]                 =141
lut["top_latte_can"]                        =142
lut["top_latte_pet"]                        =143
lut["top_the_black_can380"]                 =144
lut["toreta_can"]                           =145
lut["toreta_pet"]                           =146
lut["trevi_lemon_pet"]                      =147
lut["tropicana_apple_can"]                  =148
lut["tropicana_orange_can"]                 =149
lut["tropicana_peach_can"]                  =150
lut["v line_pet"]                           =151
lut["victoria_whitegrape_pet"]              =152
lut["vilak_pet"]                            =153
lut["virak_can"]                            =154
lut["vita500_can"]                          =155
lut["vita500_pet"]                          =156
lut["vita500_royal_pet"]                    =157
lut["vitamin_orange_pet"]                   =158
lut["vitamin_red_pet"]                      =159
lut["vtallk_blue_pet"]                      =160
lut["vtallk_pink_pet"]                      =161
lut["w_cha_pet"]                            =162
lut["welchs_can"]                           =163   










def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_xml2yolo( lut ):

    for fname in glob.glob("./labels/*.xml"):
        
        xmldoc = minidom.parse(fname)
        
        fname_out = (fname[:-4]+'.txt')

        with open(fname_out, "w") as f:

            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                # get class label
                classid =  (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    label_str = "-1"
                    print ("warning: label '%s' not in look-up table" %classid)

                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert_coordinates((width,height), b)
                #print(bb)

                f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        print ("wrote %s" % fname_out)



def main():
    convert_xml2yolo( lut )


if __name__ == '__main__':
    main()
