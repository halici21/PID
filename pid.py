import matplotlib.pyplot as plt

# Kp-Ki-Kd degerleri
Kp = 0.04
Ki = 0.01
Kd = 1.0


# baslangic mesafesi
initial_distance = 30
set_point = 150


# hedef ucagin hizi
target_plane_speed = 50
our_plane_initial_speed = 15


#sinirlar
control_signal_max = 20
control_signal_min = -20
integral_max = 50
integral_min = -50
maximum_speed = 100
minimum_speed = 1
target_minimum_speed = 10


#baslangic degerleri
integral = 0
error_last = 0  #son hata degeri
current_distance = initial_distance
our_plane_speed = our_plane_initial_speed
dt = 0.001
total_time = 400
time_1 = 0   # genel while dongusu icin kullanidigim parametre


#hedef ucaginin hizinin degismesi icin kullandigim parametreler
increase_speed = False


#bu verileri gostermek icin listelere ihtiyacimiz var
time_list = []
our_plane_speed_list = []
target_plane_speed_list = []
distance_list = []


while time_1 < total_time:
    # hata degeri
    error = set_point - current_distance

    # integral hesaplama
    integral = integral + error * dt

    # turevi hesaplama
    derivative = (error-error_last) / dt

    # verilen sinyal u(t)
    control_signal = (Kd * derivative + Ki * integral + Kp * error)

    # hedef ucagin ve bizim ucagimizin onceki hiz degerini atadim
    pre_control_signal_speed = our_plane_speed
    pre_target_plane_speed = target_plane_speed

    #listeye verileri ekleme
    target_plane_speed_list.append(target_plane_speed)
    time_list.append(time_1)
    distance_list.append(current_distance)
    our_plane_speed_list.append(our_plane_speed)

    #hedef ucagin hizi degisiyor
    # if target_plane_speed <= 10:
    #     increase_speed = True
    # elif target_plane_speed >= 80:
    #     increase_speed = False
    #
    # if increase_speed:
    #     target_plane_speed += (target_plane_speed / 100000)
    # else:
    #     target_plane_speed -= (target_plane_speed / 100001)

    # verilen sinyal u(t) için sınırları uygula
    if control_signal > control_signal_max:
        control_signal = control_signal_max
    elif control_signal < control_signal_min:
        control_signal = control_signal_min

    # integral degeri sinirlari
    if integral > integral_max:
        integral = integral_max
    elif integral < integral_min:
        integral = integral_min

    # mesafeye gore hizin degerini degistirme
    if current_distance < 0:
        #bu durumda biz onde olacagimiz icin hizi kesmesi icin cikardim
        our_plane_speed = our_plane_speed - control_signal * dt
    elif current_distance > 0:
        # hedef nokta hatadan fazla ise yavaslamasi gerekir o yuzden cikardim
        if set_point > error:
            # ucagimizin guncel hizi
            our_plane_speed = our_plane_speed - control_signal * dt
        elif set_point <= error:
            # ucagimizin guncel hizi
            our_plane_speed = our_plane_speed + control_signal * dt

    #ucagimizin hiz sinirlari
    if our_plane_speed >= maximum_speed:
         our_plane_speed = maximum_speed
    elif our_plane_speed <= minimum_speed:
         our_plane_speed = minimum_speed

    #hedef ucagin hiz sinirlari
    if target_plane_speed >= maximum_speed:
        target_plane_speed = maximum_speed
    elif target_plane_speed <= target_minimum_speed:
        target_plane_speed = target_minimum_speed

    # ucagimizin dt de gittigi yol
    our_taken_road = ((pre_control_signal_speed + our_plane_speed) / 2) * dt

    # hedef ucagin dt icerisnde aldigi yol
    target_plane_taken_road = ((pre_target_plane_speed+target_plane_speed)/2) * dt

    # guncel mesafe
    current_distance = current_distance + target_plane_taken_road - our_taken_road

    error_last = error
    time_1 += dt


#gorsellestirme
plt.figure(figsize=(10, 8)) #boyut ayarlama


#uc tane grafigi alt alta kullanacagim o yuzden 3 row olusturdum
plt.subplot(3, 1, 1)
plt.plot(time_list, distance_list, label="Gerçekleşen")
plt.axhline(set_point, color="red", linestyle="--", label="Hedeflenen")
plt.xlabel("Zaman(s)")
plt.ylabel("Mesafe(m)")
plt.title("Mesafe-Zaman")
plt.grid(linestyle='--')
plt.legend()


plt.subplot(3, 1, 2)
plt.plot(time_list, our_plane_speed_list, label="Bizim Ucagimiz")
plt.axhline(maximum_speed, color="red", linestyle="--", label="Üst-Sınır")
plt.axhline(minimum_speed, color="red", linestyle="--", label="Alt-Sınır")
plt.xlabel("Zaman(s)")
plt.ylabel("Hiz(m/s)")
plt.title("Hiz-Zaman")
plt.grid(linestyle='--')
plt.legend()


plt.subplot(3, 1, 3)
plt.plot(time_list, target_plane_speed_list, label="Hedef Uçak")
plt.axhline(maximum_speed, color="red", linestyle="--", label="Üst-Sınır")
plt.axhline(minimum_speed, color="red", linestyle="--", label="Alt-Sınır")
plt.xlabel("Zaman(s)")
plt.ylabel("Hiz(m/s)")
plt.title("Hiz-Zaman")
plt.grid(linestyle='--')
plt.legend()


plt.tight_layout()
plt.show()