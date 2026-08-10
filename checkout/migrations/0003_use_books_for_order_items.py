import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_book_rejection_reason_book_reviewed_at_and_more"),
        ("checkout", "0002_order_original_bag_order_stripe_pid_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderlineitem",
            old_name="product",
            new_name="book",
        ),
        migrations.AlterField(
            model_name="orderlineitem",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="books.book",
            ),
        ),
        migrations.RemoveField(
            model_name="orderlineitem",
            name="product_size",
        ),
        migrations.AlterField(
            model_name="orderlineitem",
            name="lineitem_total",
            field=models.DecimalField(
                decimal_places=2,
                editable=False,
                max_digits=10,
            ),
        ),
    ]