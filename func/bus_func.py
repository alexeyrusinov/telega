from func import pars_bus


def get_schedule_with_type(start_place, finish_place, days, type_schedule):
    if type_schedule == "все автобусы":
        return pars_bus.get_all_bus_schedule(start_place, finish_place, days=days)
    elif type_schedule == "отправленные":
        return pars_bus.get_bus_dispatched(start_place, finish_place, days=days)
    elif type_schedule == "отмененные":
        return pars_bus.get_bus_canceled(start_place, finish_place, days=days)
    elif type_schedule == "ближайшие":
        return pars_bus.get_current_schedule(start_place, finish_place, days=days)
