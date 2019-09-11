# coding: utf-8
from rest_framework import serializers

from plates_app.models import PersonId, Owner, NumberPlate

from django.db import transaction

from plates_app.tasks import retrieve_image


class PersonIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonId
        fields = ('id', 'id_type', 'value')


class OwnerSerializer(serializers.ModelSerializer):
    document = PersonIdSerializer()

    class Meta:
        model = Owner
        fields = ('id', 'first_name', 'last_name', 'middle_name',
                  'document')


def create_model(model, kwargs):
    return model.objects.create(**kwargs)


def make_dict(d: dict, include=(), exclude=(), add_dict=None) -> dict:
    result = {}
    _d = d.copy()
    for k, v in _d.items():
        if isinstance(v, (list, dict)):
            if k in include:
                result[k] = d.pop(k)
            elif k in exclude:
                d.pop(k)
        elif isinstance(v, str):
            if k in exclude:
                d.pop(k)
            else:
                result[k] = v
    if add_dict:
        if isinstance(add_dict, dict):
            result = {**result, **add_dict}
    return result


def add_dict_to_list(d: dict) -> []:
    _l = list()
    _l.append(d.copy())
    return _l


def serialize(serializer_class, instance, data, partial=True):
    serializer = serializer_class(instance=instance, data=data, partial=partial)
    serializer.is_valid()
    serializer.save()


class NumberPlateSerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(many=True)

    class Meta:
        model = NumberPlate
        fields = ('id', 'plates_number', 'car_model', 'model_image', 'owners')

    @transaction.atomic
    def create(self, validated_data):
        try:
            structs = make_dict(
                validated_data,
                include=['owners'],
                exclude=['model_image']
            )
            # create plates
            number_plate = create_model(NumberPlate, validated_data)
            # create owners
            if 'owners' in structs:
                owners_list = structs['owners']
                if isinstance(owners_list, dict):
                    owners_list = add_dict_to_list(owners_list)
                for o in owners_list:
                    owner = make_dict(o, add_dict={
                        'document': create_model(PersonId, o.pop('document')),
                        'plates': number_plate
                    })
                    create_model(Owner, owner)
        except Exception as e:
            raise e
        # call celery task to retrieve image
        retrieve_image.apply_async((number_plate.car_model, number_plate.id), countdown=5)
        return number_plate

    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            make_dict(
                validated_data,
                exclude=('owners', 'model_image')
            )
            # update plates
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            # update owners
            owners = self.initial_data['owners']
            if len(owners) > 0:
                owners_dict = {o.pop('id'): o for o in owners}
                for inst in instance.owners.all():
                    update_data = owners_dict[inst.id]
                    update_doc = update_data.pop('document')
                    serialize(PersonIdSerializer, instance=inst.document, data=update_doc, partial=True)
                    serialize(OwnerSerializer, instance=inst, data=update_data, partial=True)
        except Exception as e:
            raise e
        return instance

