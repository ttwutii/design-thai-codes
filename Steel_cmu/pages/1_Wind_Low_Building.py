import streamlit as st
import pandas as pd 
import numpy as np
from scipy import interpolate
from PIL import Image


st.title('มาตรฐาน มยผ.1311-50')
st.header('การคำนวณแรงลมสำหรับอาคารเตี้ย')
st.caption('### การคำนวณแรงสถิตเทียบเท่า โดยวิธีการอย่างง่าย')



inputs = st.container()
with inputs:
    st.write('### มิติอาคาร')
    col1, col2= st.columns(2)
    with col1:
        H_roof = st.number_input(label='ความสูงจั่วหลังคา, $H_\mathrm{roof} \mathrm{~[m]}$', min_value=0.0, max_value=23.0, value=9.00, step=0.1)
        H = st.number_input(label='ความสูงอาคาร (ชายคา), $H \mathrm{~[m]}$', min_value=0.0, max_value=23.0, value=6.0, step=0.1)
        
        
    with col2:
        B = st.number_input(label='ความกว้างในแนวตั้งฉากสันหลังคา, $B \mathrm{~[m]}$', min_value=0.0, value=20.0, step=0.1)
        W = st.number_input(label='ความกว้างในแนวขนานสันหลังคา, $W \mathrm{~[m]}$', min_value=0.0, value=40.0, step=0.1)
        Ds = min(B,W)
        st.write(r'ความกว้างด้านแคบที่สุด, $D_s = %.2f \mathrm{~m}$'%(Ds))
        
    with col1:
        slope = np.arctan((H_roof-H)/(0.5*B))*180.0/np.pi
        st.markdown(r'Roof slope, $\theta = %.2f \mathrm{~deg}$'%(slope))
        round(slope,2)

st.write("---")


st.write('### Check!')
col1, col2 = st.columns(2)
with col1:
    st.markdown(r'$H = %.2f$'%(H))
    st.markdown(r'$\quad\>\> H \leq 80 \mathrm{~m}$')
    st.markdown(r'$\quad\>\> %.2f \mathrm{~m} \leq 80 \mathrm{~m}$'%(H))
    if H <= 80:
        st.markdown(r'$\quad\>\>\textcolor{green}{Ok}$')
    else:
        st.markdown(r'$\quad\>\>\textcolor{red}{Not ~ Ok}$')
with col2:
    WW = H*Ds/H
    st.markdown(r'$H = %.2f$'%(H))
    st.markdown(r'$\quad\>\> \left( \frac{H}{W} \right) < 3 $')
    st.markdown(r'$\quad\>\> \left( \frac{%.2f}{%.2f} \right) < 3$'%(H,WW))
    st.markdown(r'$\quad\>\> %.2f < 3$'%(H/WW))

    if H/WW < 3:
        st.markdown(r'$\quad\>\>\textcolor{green}{Ok}$')
    else:
        st.markdown(r'$\quad\>\>\textcolor{red}{Not ~ Ok}$')


st.write("---")



#วิธีแบบInputค่าI
#I = st.number_input(label='Important Factor', min_value= 0.0, value= 1.0)
#st.write('The important factor is ', I)
#st.markdown(r"I = %.2f"%(I)) ~~~


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

if slope < 7:
    st.markdown(r'สำหรับหลังคาที่มีความชัน**น้อยกว่า 7 องศา**, ความสูงอ้างอิง, $h$, สามารถใช้ความสูงชายคา, $H$, แทนได้ แต่ต้องมีค่าไม่น้อยกว่า 6 เมตร')
    h_ = H
    h = max(h_,6.0)
    st.markdown(r'$\qquad$ ความสูงอ้างอิง, $\quad h = \max \left( H, 6.0 \mathrm{~m}  \right) = \max \left(%.2f \mathrm{~m}, 6.0 \mathrm{~m} \right) = %.2f \mathrm{~m}$'%(h_,h))
    
    z = h
    st.markdown(r'ความสูงตำแหน่งคำนวณแรงลมจากพื้นดิน, $z = h = %.2f \mathrm{~m}$'%(z))
    
else:
    st.markdown(r'สำหรับหลังคาที่มีความชัน**มากกว่า 7 องศา**, ความสูงอ้างอิง, $h$, ให้ใช้ความสูงเฉลี่ยของหลังคา แต่ต้องมีค่าไม่น้อยกว่า 6 เมตร')
    h_ = 0.5*(H_roof+H)
    h = max(h_,6.0)
    st.markdown(r'$\qquad$ ความสูงเฉลี่ยของหลังคา, $\quad H_\mathrm{avg} = 0.5 \left( H_\mathrm{roof} + H \right) = 0.5 \left( %.2f \mathrm{~m} + %.2f \mathrm{~m} \right) = %.2f \mathrm{~m}$'%(H_roof,H,h_))
    st.markdown(r'$\qquad$ ความสูงอ้างอิง, $\quad h = \max \left( H_\mathrm{avg}, 6.0 \mathrm{~m}  \right) = \max \left(%.2f \mathrm{~m}, 6.0 \mathrm{~m} \right) = %.2f \mathrm{~m}$'%(h_,h))
    
    z = h
    st.markdown(r'ความสูงตำแหน่งคำนวณแรงลมจากพื้นดิน, $z = h = %.2f \mathrm{~m}$'%(z))



    col1, buff, buff, buff, buff = st.columns(5)
with col1:
    land_type = st.selectbox(label='สภาพภูมิประเทศ', options=['แบบ A', 'แบบ B'])
    
if land_type == 'แบบ A':
    Ce = (z/10)**0.2
    st.markdown(r'$C_e = \left( \frac{z}{10} \right) ^{0.2} \ge 0.9$')
    st.markdown(r'$\quad\>\> = \left( \frac{%.2f}{10} \right) ^{0.2}$'%(z))
    st.markdown(r'$\quad\>\> = %.2f \ge 0.9$'%(Ce))
    Ce = max(Ce, 0.9)
    st.markdown(r'$\quad\>\> = %.2f$'%(Ce))
    
else:
    Ce_ = 0.7*(z/12)**0.3
    Ce = max(Ce_, 0.7)
    st.markdown(r'''$
                \begin{aligned}
                C_e &= 0.7 \left( \frac{z}{12} \right) ^{0.3} \ge 0.7 \\
                &= 0.7 \left( \frac{%.2f}{12} \right) ^{0.3} \\
                &= %.2f \ge 0.7 \\
                &= %.2f  \\
                \end{aligned}
                $'''%(z,Ce_,Ce))
    

st.write("---")

st.markdown(r'### ค่าสัมประสิทธิ์ของหน่วยแรงลมภายใน, $C_{pi} C_{gi}$')
c_gi = 2.00
st.write('สำหรับหน่วยแรงลมสถิตเทียบเท่าที่กระทำกับพื้นผิวภายในอาคาร')
st.markdown('##### ให้ใช้ค่า $C_{gi} = %.2f$'%(c_gi))

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




st.write("---")

st.markdown(r'### ค่าสัมประสิทธิ์ของหน่วยแรงลมภายนอก, $C_p C_g$')
st.markdown(r'ค่าสัมประสิทธิ์ของหน่วยแรงลมได้ถูกนำมารวมกับค่าประกอบเนื่องจากผลการกระโชกของลม')

st.write('### Check!')
col1, col2 = st.columns(2)
with col1:
    st.markdown(r'$H = %.2f$'%(H))
    st.markdown(r'$\quad\>\> H \leq 23 \mathrm{~m}$')
    st.markdown(r'$\quad\>\> %.2f \mathrm{~m} \leq 23 \mathrm{~m}$'%(H))
    if H <= 23:
        st.markdown(r'$\quad\>\>\textcolor{green}{Ok}$')
    else:
        st.markdown(r'$\quad\>\>\textcolor{red}{Not ~ Ok}$')
with col2:
    HDs = H/Ds
    st.markdown(r'$D_s = %.2f$'%(Ds))
    st.markdown(r'$\quad\>\> \left( \frac{H}{Ds} \right) < 1$')
    st.markdown(r'$\quad\>\> \left( \frac{%.2f}{%.2f} \right) < 1$'%(H,Ds))
    st.markdown(r'$\quad\>\> %.2f < 1$'%(HDs))

    if HDs < 1:
        st.markdown(r'$\quad\>\>\textcolor{green}{Ok}$')
    else:
        st.markdown(r'$\quad\>\>\textcolor{red}{Not ~ Ok}$')




#st.subheader('_แรงกระทำกรณีที่ 1 ทิศทางการพัดของลมโดยทั่วไป อยู่ในแนวตั้งฉากกับสันหลัวคา_')
df_case1 = pd.DataFrame({
    #'ความลาดชันของหลังคา (องศา)':['0-5','20','30-45','90'],
    'Slope min [deg]': [0, 20, 30, 90],
    'Slope max [deg]': [5, 20, 45, 90],
    '1':[0.75,1.0,1.05,1.05],
    '1E':[1.15,1.5,1.3,1.3],
    '2':[-1.3,-1.3,0.4,1.05],
    '2E':[-2.0,-2.0,0.5,1.3],
    '3':[-0.7,-0.9,-0.8,-0.7],
    '3E':[-1.0,-1.3,-1.0,-0.9],
    '4':[-0.55,-0.8,-0.7,-0.7],
    '4E':[-0.8,-1.2,-0.9,-0.9],
})
#st.dataframe(df_case1,hide_index=True) #ไว้ใช้แสดงตาราง

#st.subheader('_แรงกระทำกรณีที่ 2 ทิศทางการพัดของลมโดยทั่วไปอยู่ในแนวขนานกับสันหลัวคา_')
df_case2 = pd.DataFrame({
    #'ความลาดชันของหลังคา (องศา)':['0-90'],
    'Slope min [deg]': [0],
    'Slope max [deg]': [90],
    '1':[-0.85],
    '1E':[-0.9],
    '2':[-1.3],
    '2E':[-2.0],
    '3':[-0.7],
    '3E':[-1.0],
    '4':[-0.85],
    '4E':[-0.9],
    '5':[0.75],
    '5E':[1.15],
    '6':[-0.55],
    '6E':[-0.8],
})
#st.dataframe(df_case2,hide_index=True) #ไว้ใช้แสดงตาราง
 
zone_list = df_case1.columns
zone_list = ['Slope [deg]'] + zone_list[2:].to_list()

def interpolate_y(index):
    x_data = [float(df_case1['Slope max [deg]'][index]), float(df_case1['Slope min [deg]'][index+1])]
    aa = df_case1.iloc[index,2:].to_list()
    bb = df_case1.iloc[index+1,2:].to_list()
    y_all = zip(aa, bb)
    
    y_interpolate = []
    for y_data in y_all:
        f = interpolate.interp1d(x_data, y_data)
        y_interpolate.append(round(f([slope])[0],2))

    df = pd.DataFrame(data=[round(slope,2)] + y_interpolate)
    df = df.T
    df.columns = zone_list
    
    return df

if slope > 5.0 and slope < 20.0:
    df_CpCg = interpolate_y(0)
elif slope > 20.0 and slope < 30.0:
    df_CpCg = interpolate_y(1)
elif slope > 45.0 and slope < 90.0:
    df_CpCg = interpolate_y(2)
elif slope >= 0.0 and slope <= 5.0:
    df_CpCg = pd.DataFrame(data=[round(slope,2)] + df_case1.iloc[0,2:].to_list())
    df_CpCg = df_CpCg.T
    df_CpCg.columns = zone_list
elif slope == 20.0:
    df_CpCg = pd.DataFrame(data=[round(slope,2)] + df_case1.iloc[1,2:].to_list())
    df_CpCg = df_CpCg.T
    df_CpCg.columns = zone_list
elif slope >= 30.0 and slope <= 45.0:
    df_CpCg = pd.DataFrame(data=[round(slope,2)] + df_case1.iloc[2,2:].to_list())
    df_CpCg = df_CpCg.T
    df_CpCg.columns = zone_list
elif slope == 90.0:
    df_CpCg = pd.DataFrame(data=[round(slope,2)] + df_case1.iloc[3,2:].to_list())
    df_CpCg = df_CpCg.T
    df_CpCg.columns = zone_list


col1, col2 = st.columns([0.5,0.5])
with col1:
    st.markdown('##### **กรณีที่ 1:** ทิศทางการพัดของลมโดยทั่วไปอยู่ในแนว**ตั้งฉาก**กับสันหลังคา')
    st.image('CpCg_case1.png')
    st.dataframe(df_CpCg, hide_index=True, use_container_width=True)
    with st.expander('See table'):
        st.dataframe(df_case1, hide_index=True, use_container_width=True)
    
with col2:
    st.markdown('##### **กรณีที่ 2:** ทิศทางการพัดของลมโดยทั่วไปอยู่ในแนว**ขนาน**กับสันหลังคา')
    st.image('CpCg_case2.png')
    
    st.dataframe(df_case2, hide_index=True, use_container_width=True)


st.write("---")

#defind type
I = float(I)
q = float(q)
C_pi1 = float(C_pi1)
C_pi2 = float(C_pi2)
c_gi = float(c_gi)

st.markdown(r'### Net Wind Pressure,$\left( kg/m^2 \right) $')
st.markdown(r'$P_{net} = p - p_i = I_w q C_e \left(  C_g C_p - C_{gi} C_{pi}  \right)  $')

Iqce = I*q*Ce
st.markdown(r'$\quad\>\> ~~~~~~~~~~~~~~~~~ = %.2f \left(  C_g C_p - C_{gi} C_{pi}  \right)  $'%(Iqce))

st.markdown('')

col1, col2 = st.columns(2)
with col1:
    st.markdown(''' 
                สัมประสิทธิ์ที่เป็น :red[ค่าลบ] หมายถึง :red[แรงที่กระทำที่พุ่งออกและตั้งฉาก] กับพื้นผิว''')
with col2:
    st.markdown(''' 
                สัมประสิทธิ์ที่เป็น :blue[ค่าบวก] หมายถึง :blue[แรงที่กระทำที่พุงเข้าและตั้งฉาก] กับพื้นผิว''')

st.markdown('')

st.markdown(r'$ Main ~ Structure$')


tab1, tab2 = st.tabs(["Case 1", "Case 2"])

with tab1:
    st.markdown('''
            ### Wind Load Case 1 ''')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            ######  Wind direction :green[perpendicular] to the ridge & :red[Negative] Internal Pressure :orange[$Cpi = %.2f$]''' %(C_pi1) )

        zone1neg = pd.DataFrame({
    'Zone': ['1','1E','2','2E','3','3E','4','4E'],
    })

        df_CpCgcal = df_CpCg.T

        zone1neg['CgCp'] = df_CpCgcal.iloc[1:9, 0].values.flatten()
        zone1neg['Cgi'] = [c_gi]*8
        zone1neg['Cpi'] = [C_pi1]*8
        zone1neg['CgCp-CgiCpi'] = zone1neg['CgCp'] - (c_gi*C_pi1)
        zone1neg['Net Pressure'] = (I * q * Ce)*zone1neg['CgCp-CgiCpi']
        zone1neg['Net Pressure'] = zone1neg['Net Pressure'].round(2)

        st.dataframe(zone1neg, hide_index=True, use_container_width=True)

    with col2:
        st.markdown('''
           ######  Wind direction :green[perpendicular] to the ridge & :blue[Positive] Internal Pressure :orange[$Cpi = %.2f$]''' %(C_pi2) )

        zone1pos = pd.DataFrame({
    'Zone': ['1','1E','2','2E','3','3E','4','4E'],
    })

        df_CpCgcal = df_CpCg.T

        zone1pos['CgCp'] = df_CpCgcal.iloc[1:9,0].values.flatten()
        zone1pos['Cgi'] = [c_gi]*8
        zone1pos['Cpi'] = [C_pi2]*8
        zone1pos['CgCp-CgiCpi'] = zone1pos['CgCp'] - (c_gi*C_pi2)
        zone1pos['Net Pressure'] = (I * q * Ce)*zone1pos['CgCp-CgiCpi']
        zone1pos['Net Pressure'] = zone1pos['Net Pressure'].round(2)

        st.dataframe(zone1pos, hide_index=True, use_container_width=True)
    with st.expander("แสดงภาพประกอบพื้นที่ผิวที่แรงลมมากระทำ"):
        st.image('CpCg_case1.png')

with tab2:
    st.markdown('''
            ### Wind Load Case 2 ''')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
           ######  Wind direction :green[parallel] to the ridge & :red[Negative] Internal Pressure :orange[$Cpi = %.2f$]''' %(C_pi1) )

        zone2neg = pd.DataFrame({
    'Zone': ['1','1E','2','2E','3','3E','4','4E','5','5E','6','6E'],
    })

        df_CpCgcase2cal = df_case2.T

        zone2neg['CgCp'] = df_CpCgcase2cal.iloc[2:14, 0].values.flatten()
        zone2neg['Cgi'] = [c_gi]*12
        zone2neg['Cpi'] = [C_pi1]*12
        zone2neg['CgCp-CgiCpi'] = zone2neg['CgCp'] - (c_gi*C_pi1)
        zone2neg['Net Pressure'] = (I * q * Ce)*zone2neg['CgCp-CgiCpi']
        zone2neg['Net Pressure'] = zone2neg['Net Pressure'].round(2)

        st.dataframe(zone2neg, hide_index=True, use_container_width=True)

    with col2:
        
        st.markdown('''
           ######  Wind direction :green[parallel] to the ridge & :blue[Positive] Internal Pressure :orange[$Cpi = %.2f$]''' %(C_pi2) )

        zone2pos = pd.DataFrame({
    'Zone': ['1','1E','2','2E','3','3E','4','4E','5','5E','6','6E'],
    })

        df_CpCgcase2cal = df_case2.T

        zone2pos['CgCp'] = df_CpCgcase2cal.iloc[2:14, 0].values.flatten()
        zone2pos['Cgi'] = [c_gi]*12
        zone2pos['Cpi'] = [C_pi2]*12
        zone2pos['CgCp-CgiCpi'] = zone2pos['CgCp'] - (c_gi*C_pi2)
        zone2pos['Net Pressure'] = (I * q * Ce)*zone2pos['CgCp-CgiCpi']
        zone2pos['Net Pressure'] = zone2pos['Net Pressure'].round(2)

        st.dataframe(zone2pos, hide_index=True, use_container_width=True)
    with st.expander("แสดงภาพประกอบพื้นที่ผิวที่แรงลมมากระทำ"):
        st.image('CpCg_case2.png')
        


col1, col2 = st.columns(2)
with col1:
    st.markdown(r'$ Width ~ "z" ~ of ~ gable ~ wall $')
    Z = min(0.1*Ds,0.4*H)
    Z = max(Z,1,0.04*Ds)

    st.markdown(r'$z = min((0.1Ds),(0.4H)) > max((1),(0.04Ds))$')
    st.markdown(r'$z = %.2f \mathrm{~m} $'%(Z))
   
with col2:
    st.markdown(r'$Width ~ "y"~  of ~ end ~ zone$')
    Y = max(6,2*Z)
    st.markdown(r'$y = max(6,(2z))$')
    st.markdown(r'$y = %.2f \mathrm{~m} $'%(Y))
    st.write('---')
    st.markdown(r'$- ~  For ~  buildings  ~ constructed  ~ from ~  many ~  frames ~  assembled$')
    Bay = st.number_input(label='$First ~  Interior  ~ Frame \mathrm{~[m]}$', min_value=0.0, value=6.0, step=0.1)
    st.markdown(r'$ y = %.2f \mathrm{~m} $'%(Bay))


st.write('---')