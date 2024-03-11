import streamlit as st
import pandas as pd 
import numpy as np
from scipy import interpolate
from PIL import Image
import altair as alt


st.title('มาตรฐาน มยผ.1311-50')
st.header('การคำนวณแรงลมสำหรับอาคารสูง')
st.caption('### การคำนวณแรงสถิตเทียบเท่า โดยวิธีการอย่างง่าย')



inputs = st.container()
with inputs:
    st.write('### มิติอาคาร')
    col1, col2,col3 = st.columns([0.4,0.2,0.4])
    with col2:
        Floor = st.number_input(label='จำนวนชั้น',min_value=1, max_value=20, value=10,step=1)
    
    
    with col3:
        Floor_list = []
        H = 0
        Widthx_list = []
        Wx = 0
        Widthy_list = []
        Wy = 0
        for i in range(Floor):
            col1x,col2x,col3x = st.columns(3)
            with col1x:
                Heigth = st.number_input(label=r'$ความสูงของชั้นที่ \quad %i \quad \mathrm{~[m]} $'%(i+1),min_value=0.0,value=3.0,step=0.1,key=f"floor{i}")
                H = Heigth + H
                if H > 80:
                    st.markdown(r'$ H ~ > ~ 80 :ให้ไปใช้วิธีการอย่างละเอียด $')
                    
                    break
                Floor_list.append(H)
            #st.dataframe(Floor_list,hide_index=True) #ไว้ใช้แสดงตาราง
    with col1:
        Wx = st.number_input(label='ความกว้างขนานแกน $x \mathrm{~[m]}$', min_value=0.0, value=20.0, step=0.1)
        Wy = st.number_input(label='ความกว้างขนานแกน $y \mathrm{~[m]}$', min_value=0.0, value=20.0, step=0.1)
        Ds = min(Wy,Wx)
        st.write(r'ความกว้างด้านแคบที่สุด, $D_s = %.2f \mathrm{~m}$'%(Ds))
        
            
st.write("---")


#df= data frame
df_important = pd.DataFrame({
    'ประเภทความสำคัญของอาคาร': ['น้อย' , 'ปกติ', 'มาก' ,'สูงมาก'],
    'สภาวะด้านกำลัง':[0.8 , 1.0 , 1.1, 1.15],
    'สภาวะด้านการใช้งาน':[0.75, 0.75, 0.75, 0.75],
})
#st.dataframe(df_important,hide_index=True) #ไว้ใช้แสดงตาราง

df_wind_speed = pd.DataFrame({
    'กลุ่ม':['1','2','3','4A','4B'],
    'V50 [m/s]':[25,27,29,25,25],
    'T_F':[1.0,1.0,1.0,1.2,1.08],
})
#st.dataframe(df_wind_speed,hide_index=True) #ไว้ใช้แสดงตาราง

col1, col2 = st.columns(2)
with col1:
    st.write('### ค่าประกอบความสำคัญของแรงลม, $I_w$')
    col1x, col2x, col3x = st.columns(3)
    with col1x:
        important_type = st.selectbox(label='ประเภทความสำคัญ', options=df_important['ประเภทความสำคัญของอาคาร'])
    with col2x:
        cal_type = st.selectbox(label='ประเภทการออกแบบ', options=['สภาวะด้านกำลัง', 'สภาวะด้านการใช้งาน'])
    with col3x:
        I = df_important.loc[df_important['ประเภทความสำคัญของอาคาร'] == important_type, cal_type]
        st.markdown('')
        st.markdown('')
        st.markdown(r'$I = %.2f$'%(I))

    with st.expander("See table"):
        st.dataframe(df_important, hide_index=True)


with col2:
    st.write('### ความเร็วลมอ้างอิง, $\overline{V}$')
 
    area_group = st.selectbox(label='กลุ่มพื้นที่', options=df_wind_speed['กลุ่ม'])

    V50 = df_wind_speed.loc[df_wind_speed['กลุ่ม'] == area_group, 'V50 [m/s]']
    T_F = df_wind_speed.loc[df_wind_speed['กลุ่ม'] == area_group, 'T_F']
        
    if cal_type == 'สภาวะด้านกำลัง':
        V = V50*T_F
        st.markdown(r'$V_{50} = %.2f \mathrm{~m/s}, \quad T_F = %.2f$'%(V50, T_F))
        st.markdown(r'$\overline{V} = V_{50} T_F = %.2f \times %.2f = %.2f \mathrm{~m/s}$'%(V50, T_F, V))
    else:
        V = V50
        st.markdown(r'$V_{50} = %.2f \mathrm{~m/s}$'%(V50))
        st.markdown(r'$\overline{V} = V_{50} T_F = %.2f \mathrm{~m/s}$'%(V))

    with st.expander("see more"):
        tab1, tab2= st.tabs(["Table", "พื้นที่ตั้งอาคาร"])
    with tab1:
        st.dataframe(df_wind_speed, hide_index=True)
    with tab2:
        st.image("wind1.png")
        st.image("wind2.png")

st.write("---")


st.write('### หน่วยแรงลมอ้างอิง,Reference Verocity Pressure, $q$')

col1, col2 = st.columns(2)
with col1:
    rho = 1.25
    g = 9.81
    q = 0.5*rho/g*(V**2)
    st.markdown(r'ความหนาแน่นของมวลอากาศ, $\rho \approx 1.25 \mathrm{~kg/m^3}$')
with col2:
    st.markdown(r'อัตราเร่งเนื่องจากแรงโน้มถ่วงของโลก, $g = 9.81 \mathrm{~m/s^2}$')

st.markdown(r'$q = \frac{1}{2} \left( \frac{\rho}{g} \right) \overline{V}^{2} = \frac{1}{2} \left( \frac{%.2f \mathrm{~kg/m^3}}{%.2f \mathrm{~m/s^2}} \right) \left( %.2f \mathrm{~m/s} \right)^{2} = %.2f \mathrm{~kg/m^2}$'%(rho,g,V,q))


st.write("---")

st.markdown(r'### ค่าประกอบเนื่องจากสภาพภูมิประเทศ,Exposure Coefficient, $C_e$')
land_type = st.selectbox(label='สภาพภูมิประเทศ', options=['แบบ A', 'แบบ B'])


floors = pd.DataFrame({
    'ชั้นที่':[],
})
for i in range(Floor):
    floors.loc[i+1]=i+1


col1, col2, col3 = st.columns(3)
with col1:
   
    st.markdown(r'$C_e$ For Windward  walls ')
    st.markdown(r'ใช้ความสูงอ้างอิง = z(ความสูงเหนือพื้นดิน)')


    with st.expander(label = 'แสดงรายการคำนวณของค่าCeที่แต่ละความสูง'):
        Ce_winwardlist = []
        if land_type == 'แบบ A':
            for i in Floor_list:
                Ce1 = (i/10)**0.2
                st.markdown(r'$C_e = \left( \frac{z}{10} \right) ^{0.2} \ge 0.9$')
                st.markdown(r'$\quad\>\> = \left( \frac{%.2f}{10} \right) ^{0.2}$'%(i))
                st.markdown(r'$\quad\>\> = %.2f \ge 0.9$'%(Ce1))
                Ce1 = max(Ce1, 0.9)
                st.markdown(r'$\quad\>\> = %.2f$'%(Ce1))
                Ce_winwardlist.append(Ce1)
    
        else:
            for i in Floor_list:
                Ce_ = 0.7*(i/12)**0.3
                Ce1 = max(Ce_, 0.7)
                st.markdown(r'''$
                \begin{aligned}
                C_e &= 0.7 \left( \frac{z}{12} \right) ^{0.3} \ge 0.7 \\
                &= 0.7 \left( \frac{%.2f}{12} \right) ^{0.3} \\
                &= %.2f \ge 0.7 \\
                &= %.2f  \\
                \end{aligned}
                $'''%(i,Ce_,Ce1))
                Ce_winwardlist.append(Ce1)
    Ce_table = pd.DataFrame(floors)
    Ce_table['ความสูงจากพื้นดิน'] = Floor_list
    Ce_table['Ce'] = Ce_winwardlist
    Ce_table['Ce'] = Ce_table['Ce'].round(2)        
    st.dataframe(Ce_table,hide_index=True,use_container_width=True)


with col2:

    st.markdown(r'$C_e$ For Leeward  walls and Internal Pressure ')
    st.markdown(r'ใช้ความสูงอ้างอิง = 0.5H')

    z = 0.5*H
    if land_type == 'แบบ A':
        Ce2 = (z/10)**0.2
        st.markdown(r'$C_e = \left( \frac{z}{10} \right) ^{0.2} \ge 0.9$')
        st.markdown(r'$\quad\>\> = \left( \frac{%.2f}{10} \right) ^{0.2}$'%(z))
        st.markdown(r'$\quad\>\> = %.2f \ge 0.9$'%(Ce2))
        Ce2 = max(Ce2, 0.9)
        st.markdown(r'$\quad\>\> = %.2f$'%(Ce2))
    
    else:
        Ce_ = 0.7*(z/12)**0.3
        Ce2 = max(Ce_, 0.7)
        st.markdown(r'''$
                \begin{aligned}
                C_e &= 0.7 \left( \frac{z}{12} \right) ^{0.3} \ge 0.7 \\
                &= 0.7 \left( \frac{%.2f}{12} \right) ^{0.3} \\
                &= %.2f \ge 0.7 \\
                &= %.2f  \\
                \end{aligned}
                $'''%(z,Ce_,Ce2))
        
with col3:

    st.markdown(r'$C_e$ For Roof and Side walls ')
    st.markdown(r'ใช้ความสูงอ้างอิง = H')

    z = H
    if land_type == 'แบบ A':
        Ce3 = (z/10)**0.2
        st.markdown(r'$C_e = \left( \frac{z}{10} \right) ^{0.2} \ge 0.9$')
        st.markdown(r'$\quad\>\> = \left( \frac{%.2f}{10} \right) ^{0.2}$'%(z))
        st.markdown(r'$\quad\>\> = %.2f \ge 0.9$'%(Ce3))
        Ce3 = max(Ce3, 0.9)
        st.markdown(r'$\quad\>\> = %.2f$'%(Ce3))
    
    else:
        Ce_ = 0.7*(z/12)**0.3
        Ce3 = max(Ce_, 0.7)
        st.markdown(r'''$
                \begin{aligned}
                C_e &= 0.7 \left( \frac{z}{12} \right) ^{0.3} \ge 0.7 \\
                &= 0.7 \left( \frac{%.2f}{12} \right) ^{0.3} \\
                &= %.2f \ge 0.7 \\
                &= %.2f  \\
                \end{aligned}
                $'''%(z,Ce_,Ce3))
    
    

st.write("---")

st.markdown(r'### ค่าประกอบเนื่องจากการกระโชกของลม, $C_g ~ and ~ C_{gi}$')
c_g = 2.00
c_gclad = 2.50
c_gi = 2.00
col1, col2 = st.columns(2)
with col1:
    st.write('###### ก. สำหรับหน่วยแรงลมสถิตเทียบเท่าที่กระทำกับพื้นผิวภายนอกอาคาร')
    st.write('- โครงสร้างหลักต้านทานแรงลม')
    st.markdown('##### ให้ใช้ค่า $C_{g} = %.2f$ '%(c_g))

    st.write('###### ข. สำหรับหน่วยแรงลมสถิตเทียบเท่าที่กระทำกับพื้นผิวภายนอกอาคาร')
    st.write('- โครงสร้างรองและผนังภายนอก(Cladding)ที่มีขนาดเล็ก')
    st.markdown('##### ให้ใช้ค่า $C_{g} = %.2f$ '%(c_gclad))
with col2:
    st.write('###### สำหรับหน่วยแรงลมสถิตเทียบเท่าที่กระทำกับพื้นผิวภายในอาคาร')
    st.markdown('##### ให้ใช้ค่า $C_{gi} = %.2f$'%(c_gi))

st.write("---")

st.write('### ค่าสัมประสิทธิ์ของหน่วยแรงลม, $C_p ~ and ~ C_{pi}$')

st.write('### Check!')
col1, col2 = st.columns(2)
with col1:
    st.markdown(r'$H = %.2f$'%(H))
    st.markdown(r'$\quad\>\> H > 23 \mathrm{~m}$')
    st.markdown(r'$\quad\>\> %.2f \mathrm{~m} > 23 \mathrm{~m}$'%(H))
    if H>23:
        st.markdown(r'$\quad\>\>\textcolor{green}{Ok}$')
    else:
        st.markdown(r'$\quad\>\>\textcolor{red}{Not ~ Ok}$')
with col2:
    HDs = H/Ds
    st.markdown(r'$D_s = %.2f$'%(Ds))
    st.markdown(r'$\quad\>\> \left( \frac{H}{Ds} \right) \geq 1$')
    st.markdown(r'$\quad\>\> \left( \frac{%.2f}{%.2f} \right) \geq 1$'%(H,Ds))
    st.markdown(r'$\quad\>\> %.2f \geq 1$'%(HDs))

    if HDs >= 1:
        st.markdown(r'$\quad\>\>\textcolor{green}{Ok}$')
    else:
        st.markdown(r'$\quad\>\>\textcolor{red}{Not ~ Ok}$')
col1, col2,col3 = st.columns([0.1,0.4,0.5])
with col2:
    st.image('Cp_high.png',caption='รูปที่ ข.9',use_column_width=True)

Dx = Wx
Dy = Wy

col1, col2 = st.columns(2)
cal1 = H/Dx
with col1:
    st.markdown(r'### ด้านขนานแกน $~ x$')
    st.markdown(r'$\quad \quad H/D_x = %.2f / %.2f  = %.2f$'%(H,Dx,cal1))
    st.markdown(r'$-Windward ~ walls$')
    if cal1 <= 0.25:
        C_px1 = 0.60
        st.markdown(r'$\quad C_p = %.2f $'%(C_px1))
    elif 0.25<cal1<1:
        C_px1 = 0.27*(cal1+2)
        st.markdown(r'$\quad C_p = %.2f $'%(C_px1))
    elif cal1 >= 1:
        C_px1 = 0.80
        st.markdown(r'$\quad C_p = %.2f $'%(C_px1))

    st.markdown(r'$-Leeward ~ walls$')
    if cal1 <= 0.25:
        C_px2 = -0.30
        st.markdown(r'$\quad C_p = %.2f $'%(C_px2))
    elif 0.25<cal1<1:
        C_px2 = -0.27*(cal1+0.88)
        st.markdown(r'$\quad C_p = %.2f $'%(C_px2))
    elif cal1 >= 1:
        C_px2 = -0.50
        st.markdown(r'$\quad C_p = %.2f $'%(C_px2))



cal2 = H/Dy
with col2:
    st.markdown(r'### ด้านขนานแกน$~ y$')
    st.markdown(r'$\quad \quad H/D_y = %.2f / %.2f  = %.2f$'%(H,Dy,cal2))

    st.markdown(r'$-Windward ~ walls$')
    if cal2 <= 0.25:
        C_py1 = 0.60
        st.markdown(r'$\quad C_p = %.2f $'%(C_py1))
    elif 0.25<cal2<1:
        C_py1 = 0.27*(cal2 + 2)
        st.markdown(r'$\quad C_p = %.2f $'%(C_py1))
    elif cal2 >= 1:
        C_py1 = 0.80
        st.markdown(r'$\quad C_p = %.2f $'%(C_py1))

    st.markdown(r'$-Leeward ~ walls$')
    if cal2 <= 0.25:
        C_py2 = -0.30
        st.markdown(r'$\quad C_p = %.2f $'%(C_py2))
    elif 0.25<cal2<1:
        C_py2 = -0.27*(cal2+0.88)
        st.markdown(r'$\quad C_p = %.2f $'%(C_py2))
    elif cal2 >= 1:
        C_py2 = -0.50
        st.markdown(r'$\quad C_p = %.2f $'%(C_py2))


st.markdown('')
st.markdown('')

df_c_pi = pd.DataFrame({
    'กรณี':['กรณีใช้กับอาคารที่ปราศจากช่องเปิดขนาดใหญ่','กรณีใช้กับอาคารที่มีการรั่วซึมซึ่งกระจายไม่สม่ำเสมอ','กรณีใช้กับอาคารที่มีช่องเปิดขนาดใหญ่'],
    'C_pi-':[-0.15,-0.45,-0.7],
    'C_pi+':[0,0.3,0.7]
    })
#st.dataframe(df_c_pi,hide_index=True) #ไว้ใช้แสดงตาราง
c_pi = st.selectbox(label='$C_{pi}$ : ค่าสัมประสิทธิ์ของหน่วยแรงลมภายใน ', options=df_c_pi['กรณี'])
C_pi1 = df_c_pi.loc[df_c_pi['กรณี'] == c_pi, 'C_pi-']
C_pi2 = df_c_pi.loc[df_c_pi['กรณี'] == c_pi, 'C_pi+']

if c_pi == 'กรณีใช้กับอาคารที่ปราศจากช่องเปิดขนาดใหญ่' :
        st.markdown(''' 
                    :orange[เช่น คลังสินค้าที่ไม่มีหน้าต่างหรือช่องเปิด โดยที่ประตูต้องออกแบบให้สามารถต้านพายุได้ และได้รับการปิดสนิมเมื่อเกิดพายุ]''')
elif c_pi == 'กรณีใช้กับอาคารที่มีการรั่วซึมซึ่งกระจายไม่สม่ำเสมอ' :
        st.markdown(''' 
                    :orange[เช่น อาคารขนาดเล็กทั่วๆไป และอาคารสูงที่มีหน้าต่างซึ่งสามารถเปิด-ปิดได้ หรือมีระเบียงซึ่งมีประตูที่สามารถเปิด-ปิดได้]''')
elif c_pi == 'กรณีใช้กับอาคารที่มีช่องเปิดขนาดใหญ่' :
        st.markdown(''' 
                    :orange[เช่น อาคารโรงงานอุตสาหกรรมและคลังสินค้าที่ประตูอาจจะเปิดในระหว่างเกิดพายุ หรือประตูไม่สามารถต้านพายุได้]''')

col1, col2 = st.columns(2)
with col1:
    st.markdown(r'$C_{pi}^{-} = %.2f$'%(C_pi1))
with col2:
    st.markdown(r'$C_{pi}^{+} = %.2f$'%(C_pi2))

st.write('---')

st.markdown(r'### Net Wind Pressure,$\left( kg/m^2 \right) $')
st.markdown(r'$P_{net} = p - p_i = I_w q C_e \left(  C_g C_p - C_{gi} C_{pi}  \right)  $')

I = float(I)
q = float(q)
C_pi1 = float(C_pi1)
C_pi2 = float(C_pi2)
c_gi = float(c_gi)

tab1, tab2 = st.tabs(["ด้านขนานแกน x", "ด้านขนานแกน y"])
with tab1:
    st.markdown(r'### $P_{xx}$')
    st.markdown(r'$Windward + Leeward = Combine ~wind$')
    col1,col2 = st.columns(2)
    with col1:
        
        st.markdown('$\quad With \quad Cpi = %.2f$' %(C_pi1) )

        Windward_x1 = pd.DataFrame(floors)
        Windward_x1['ความสูงจากพื้นดิน'] = Floor_list
        Windward_x1['Windward Net Pressure'] = (I * q * Ce_table['Ce'])*((c_g*C_px1)-(c_gi*C_pi1))
        Windward_x1['Windward Net Pressure'] = Windward_x1['Windward Net Pressure'].round(2)
        Windward_x1['Leeward Net Pressure'] = (I * q * Ce2)*((c_g*C_px2)-(c_gi*C_pi1))
        Windward_x1['Leeward Net Pressure'] = Windward_x1['Leeward Net Pressure'].round(2)
        Windward_x1['Combine wind pressure'] =  abs(Windward_x1['Windward Net Pressure'])+ abs(Windward_x1['Leeward Net Pressure'])

        st.dataframe(Windward_x1,hide_index=True,use_container_width=True)

        # สร้างกราฟด้วย Altair
        chartnet_negx = alt.Chart(Windward_x1).mark_bar(size=Floor*5, color='white', stroke='blue', strokeWidth=1).encode(
        x=alt.X('Combine wind pressure', title='Combine wind pressure'),
        y=alt.Y('ความสูงจากพื้นดิน', title='ความสูงจากพื้นดิน'),
        ).configure_mark(orient='horizontal').properties(
        height=Floor*70
        )

        # แสดงกราฟด้วย st.altair_chart()
        st.altair_chart(chartnet_negx, use_container_width=True)


    
    with col2:
        st.markdown('$\quad With \quad Cpi = %.2f$' %(C_pi2) ) 
       
        Windward_x2 = pd.DataFrame(floors)
        Windward_x2['ความสูงจากพื้นดิน'] = Floor_list
        Windward_x2['Windward Net Pressure'] = (I * q * Ce_table['Ce'])*((c_g*C_px1)-(c_gi*C_pi2))
        Windward_x2['Windward Net Pressure'] = Windward_x2['Windward Net Pressure'].round(2)
        Windward_x2['Leeward Net Pressure'] = (I * q * Ce2)*((c_g*C_px2)-(c_gi*C_pi2))
        Windward_x2['Leeward Net Pressure'] = Windward_x2['Leeward Net Pressure'].round(2)
        Windward_x2['Combine wind pressure'] =  abs(Windward_x2['Windward Net Pressure'])+ abs(Windward_x2['Leeward Net Pressure'])



        st.dataframe(Windward_x2,hide_index=True,use_container_width=True)
        
        # สร้างกราฟด้วย Altair
        chartnet_negx = alt.Chart(Windward_x2).mark_bar(size=Floor*5, color='white', stroke='blue', strokeWidth=1).encode(
        x=alt.X('Combine wind pressure', title='Combine wind pressure'),
        y=alt.Y('ความสูงจากพื้นดิน', title='ความสูงจากพื้นดิน'),
        ).configure_mark(orient='horizontal').properties(
        height=Floor*70
        )

        # แสดงกราฟด้วย st.altair_chart()
        st.altair_chart(chartnet_negx, use_container_width=True)



with tab2:
    st.markdown(r'### $P_{yy}$')
    st.markdown(r'$Windward + Leeward = Combine ~wind$')
    col1,col2 = st.columns(2)
    with col1:
        
        st.markdown('$\quad With \quad Cpi = %.2f$' %(C_pi1) )

        Windward_y1 = pd.DataFrame(floors)
        Windward_y1['ความสูงจากพื้นดิน'] = Floor_list
        Windward_y1['Windward Net Pressure'] = (I * q * Ce_table['Ce'])*((c_g*C_py1)-(c_gi*C_pi1))
        Windward_y1['Windward Net Pressure'] = Windward_y1['Windward Net Pressure'].round(2)
        Windward_y1['Leeward Net Pressure'] = (I * q * Ce2)*((c_g*C_py2)-(c_gi*C_pi1))
        Windward_y1['Leeward Net Pressure'] = Windward_y1['Leeward Net Pressure'].round(2)
        Windward_y1['Combine wind pressure'] =  abs(Windward_y1['Windward Net Pressure'])+ abs(Windward_y1['Leeward Net Pressure'])


        st.dataframe(Windward_y1,hide_index=True,use_container_width=True)

         # สร้างกราฟด้วย Altair
        chartnet_negx = alt.Chart(Windward_y1).mark_bar(size=Floor*5, color='white', stroke='blue', strokeWidth=1).encode(
        x=alt.X('Combine wind pressure', title='Combine wind pressure'),
        y=alt.Y('ความสูงจากพื้นดิน', title='ความสูงจากพื้นดิน'),
        ).configure_mark(orient='horizontal').properties(
        height=Floor*70
        )

        # แสดงกราฟด้วย st.altair_chart()
        st.altair_chart(chartnet_negx, use_container_width=True)


        

    
    with col2:
        st.markdown('$\quad With \quad Cpi = %.2f$' %(C_pi2) ) 
       
        Windward_y2 = pd.DataFrame(floors)
        Windward_y2['ความสูงจากพื้นดิน'] = Floor_list
        Windward_y2['Windward Net Pressure'] = (I * q * Ce_table['Ce'])*((c_g*C_py1)-(c_gi*C_pi2))
        Windward_y2['Windward Net Pressure'] = Windward_y2['Windward Net Pressure'].round(2)
        Windward_y2['Leeward Net Pressure'] = (I * q * Ce2)*((c_g*C_py2)-(c_gi*C_pi2))
        Windward_y2['Leeward Net Pressure'] = Windward_y2['Leeward Net Pressure'].round(2)
        Windward_y2['Combine wind pressure'] =  abs(Windward_y2['Windward Net Pressure'])+ abs(Windward_y2['Leeward Net Pressure'])


        st.dataframe(Windward_y2,hide_index=True,use_container_width=True)

         # สร้างกราฟด้วย Altair
        chartnet_negx = alt.Chart(Windward_y2).mark_bar(size=Floor*5, color='white', stroke='blue', strokeWidth=1).encode(
        x=alt.X('Combine wind pressure', title='Combine wind pressure'),
        y=alt.Y('ความสูงจากพื้นดิน', title='ความสูงจากพื้นดิน'),
        ).configure_mark(orient='horizontal').properties(
        height=Floor*70
        )

        # แสดงกราฟด้วย st.altair_chart()
        st.altair_chart(chartnet_negx, use_container_width=True)


        


   
st.write('---')
        






