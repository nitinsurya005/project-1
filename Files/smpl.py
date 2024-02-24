l={'Bill': 0, 'Invoice No. ': 21, 'Date': 27, 'Delivery Note ': 49, 'Mode/Terms of Payment ': 55, "Buyer's Order No. ": 77, 'Dated': 83, 'Shipping Address ': 99, 'Dispatch Doc No. ': 105, 'Delivery Note Date ': 111, 'Dispatched through ': 133, 'Destination': 139, 'Bill of Lading/LR-RR No. ': 161, 'Motor Vehicle No. ': 167, 'Buyer (Bill to) ': 183, 'Terms of Delivery ': 189, 'SL NO ': 211, 'ITEM / DESCRIPTION ': 212, 'HSN/SAC': 217, 'QUANTITY': 218, 'RATE': 221, 'UOM': 222, 'AMOUNT': 224, 'TOTAL': 238, 'Amount Chargeable (in words) ': 253, 'CGSTP': 283, 'CGST': 285, 'SGSTP': 297, 'SGST': 299, 'IGSTP': 311, 'IGST': 313, 'ITOTAL': 327}
print(l.values())
# import os
# from sqlite3 import *
# o=os.getcwd()
# con=connect(o+'\\addbook.db')
# cur=con.cursor()
# # c̥ur.execute('create table addbook(sno int, name varchar(100) NOT NULL, ad varchar(1000000000) NOT NULL,gstin varchar(100) primary key, stc varchar(10000) NOT NULL)')
# cur.execute('delete from addbook where sno>0')
# con.commit()
# con.close()
# l=['1', '2', '3', '4', '5', '6', 'SRT TRADER\nNo.45-A, Pudupalayam,\nKamaraj Nagar,\nMuthur - 638105.', '7', '8', '9', '10', '11', '12', 'SRT TRADER\nNo.45-A, Pudupalayam,\nKamaraj Nagar,\nMuthur - 638105.', '', '1.\n2.', 'coconut\nshell', '0801\n0000', '10000\n1000', '10\n2', 'pcs\npcs', '100000\n2000', 'One lakh Sixty Three Thousand Two Hundred Rupees Only', '10', 10200, '20', 20400, '30', 163200]
# a=['Invoice No.','Date','Delivery Note','Mode/Terms of Payment',"Buyer's Order No.",'Dated','Shipping Address','Dispatch Doc No.','Delivery Note Date','Dispatched through ','Destination','Bill of Lading/LR-RR No.','Motor Vehicle No.','Buyer (Bill to)','Terms of Delivery','SL NO','ITEM / DESCRIPTION','HSN/SAC','QUANTITY','RATE','UOM','AMOUNT','TOTAL','Amount Chargeable (in words)','CGSTP','CGST','SGSTP','SGST','IGSTP','IGST','ITOTAL']
# for i in range(len(l)):print(f"{a[i]} = {l[i]}")
# print(len(l),len(a))