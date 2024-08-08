from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub')
    image = models.ImageField(blank=True, null=True, upload_to='media/category')
    slug = models.SlugField(blank=True, null=True)
    show_in_home = models.BooleanField(help_text='Are the products of this category displayed on the main page?',
                                       verbose_name='show product in home')
    show_in_home_no_product = models.BooleanField(default=False, verbose_name='show image in home')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
        return ('no image')


class Image(models.Model):
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.CASCADE,
                                related_name='images_related')
    image = models.ImageField(upload_to='product-img', verbose_name='image')
    alt = models.CharField(max_length=500, null=True, blank=True, verbose_name='image alt')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return str(self.image)


class Tag(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)
    body = RichTextField()
    price = models.IntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='discount percent')
    images = models.ManyToManyField(Image, null=True, blank=True, related_name='post_images',
                                    verbose_name='Product photos')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, null=True, blank=True, related_name='post_tag')
    slug = models.SlugField(allow_unicode=True, unique=True)
    sold = models.PositiveIntegerField(default=0, verbose_name='Quantity sold')
    view = models.IntegerField(default=1)

    def increase_sold(self, quantity):
        self.sold += quantity
        self.save()

    def show_discount(self):
        if self.discount:
            return (f'yes: %{self.discount}')
        return ('no')

    show_discount.short_description = 'تخفیف'

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='product_attributes', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product.name} - {self.attribute.name}: {self.value}'

# class CommentProducts(models.Model):
#     product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='comments',
#                                 )
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#     name = models.CharField(max_length=50, null=True)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply',
#                                verbose_name="ریپلای")
#     text = models.TextField(null=True, verbose_name="متن")
#     created = jmodels.jDateTimeField(auto_now_add=True)
#     user_admin = models.BooleanField(default=False, verbose_name='ادمین بودن کاربر')
#     accepetd = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.text
#
#     class Meta:
#         verbose_name = 'کامت محصول'
#         verbose_name_plural = 'کامنت های محصول'
