from PIL import Image
import matplotlib.pyplot as plt

# 이미지 열기
r = Image.open('/Users/mzc01-ptty/Desktop/Desktop/Velog/cka.png')
m_size=10 #픽셀 크기 지정
for i in range(0, r.size[0],m_size): # range안에 (시작, 끝, 단위) 이렇게도 넣을 수 있음
    for j in range(0, r.size[1],m_size):
        r.putpixel((i,j),(0,0,0))

plt.imshow(r)
plt.show()
r_sum = 0
g_sum = 0
b_sum = 0
for i in range(0, r.size[0], m_size):
    for j in range(0, r.size[1], m_size):
        r_sum = 0
        g_sum = 0
        b_sum = 0
        for ii in range(i, min(i + m_size, r.size[0])):
            for jj in range(j, min(j + m_size, r.size[1])):
                rgb = r.getpixel((ii, jj))
                r_sum += rgb[0]
                g_sum += rgb[1]
                b_sum += rgb[2] #RGB 값을 뽑아서 r_sum, g_sum, b_sum에 저장
        r_a = round(r_sum / m_size ** 2) #m_size 10의 제곱이 100이므로 평균을 구하는 법
        g_a = round(g_sum / m_size ** 2)
        b_a = round(b_sum / m_size ** 2)
        for ii in range(i, min(i + m_size, r.size[0])):
            for jj in range(j, min(j + m_size, r.size[1])):
                r.putpixel((ii, jj), (r_a, g_a, b_a))


plt.imshow(r)
plt.show()